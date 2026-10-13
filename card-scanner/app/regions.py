"""Locate the 8 clue text regions inside an already-warped card image.

Per the brief: do not slice the card into 8 fixed-height rectangles, since
the number of lines per clue (and the font size) varies from card to card.
Instead, anchor on the numbered bullet markers (the small filled dark-green
circles printed to the left of every clue) and use their vertical positions
to delimit each clue's region. This is robust to 1-4 line clues and to
font-size changes, since it never assumes a fixed line height.
"""

from __future__ import annotations

from dataclasses import dataclass

import cv2
import numpy as np


@dataclass
class ClueRegion:
    index: int  # 0-based
    top: int
    bottom: int
    image: np.ndarray  # crop of the body region, full width from after the bullet


@dataclass
class BulletBox:
    x: int
    y: int
    w: int
    h: int

    @property
    def cy(self) -> int:
        return self.y + self.h // 2


def find_body_top(card_bgr: np.ndarray, search_fraction: float = 0.45) -> int:
    """Find the row where the dark green header ends and the white body starts.

    Scans the mean brightness per row (restricted to the central band to
    avoid rounded-corner/background bleed at the sides) and returns the
    first row that begins a sustained bright run.
    """
    h, w = card_bgr.shape[:2]
    x0, x1 = int(w * 0.15), int(w * 0.85)
    search_h = int(h * search_fraction)
    gray = cv2.cvtColor(card_bgr[:search_h, x0:x1], cv2.COLOR_BGR2GRAY)
    row_mean = gray.mean(axis=1)

    bright = row_mean > 140
    run_needed = max(10, search_h // 40)
    run = 0
    for y in range(len(bright)):
        if bright[y]:
            run += 1
            if run >= run_needed:
                return max(0, y - run_needed + 1)
        else:
            run = 0
    # Fallback: header not confidently found, assume a conservative default.
    return int(h * 0.15)


def _bullet_mask(body_bgr: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(body_bgr, cv2.COLOR_BGR2GRAY)

    # Plain Otsu over the whole body is too generous here: the perspective
    # warp maps the card's rounded corners into the output rectangle's
    # corners, leaving a blurry card/background transition there (a
    # desaturated mid-gray, not a clean dark ink and not a clean light
    # background). That blur sits *between* true ink and white card stock,
    # so a global bimodal split (Otsu) pulls its threshold high enough to
    # swallow the blur as "ink" too. True ink (bullet fill, glyph strokes)
    # is reliably much darker than that blur, so calibrate off the body's
    # own darkest pixels (bullets/text are a small minority of the body)
    # instead of trusting Otsu's midpoint.
    dark_reference = float(np.percentile(gray, 5))
    ink_threshold = min(150.0, max(50.0, dark_reference * 3.0))
    _, mask = cv2.threshold(gray, ink_threshold, 255, cv2.THRESH_BINARY_INV)

    # Background (and the blur above) leans reddish; ink is neutral/dark
    # green. Cheap extra safety net on top of the stricter threshold.
    b = body_bgr[:, :, 0].astype(np.int16)
    g = body_bgr[:, :, 1].astype(np.int16)
    r = body_bgr[:, :, 2].astype(np.int16)
    background_like = ((r - g) > 15).astype(np.uint8) * 255
    mask = cv2.bitwise_and(mask, cv2.bitwise_not(background_like))
    return mask


def find_bullets(body_bgr: np.ndarray, left_band_fraction: float = 0.22) -> list[BulletBox]:
    h, w = body_bgr.shape[:2]
    mask = _bullet_mask(body_bgr)

    band_w = int(w * left_band_fraction)
    band_mask = np.zeros_like(mask)
    band_mask[:, :band_w] = mask[:, :band_w]

    contours, _ = cv2.findContours(band_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Rough, card-independent ballpark just to pick initial candidates; the
    # real reference size is calibrated per-card below, since bullet size
    # (like clue font size) varies from card to card.
    rough_d = w * 0.055
    min_area = (rough_d * 0.5) ** 2

    candidates = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        x, y, cw, ch = cv2.boundingRect(c)
        if cw < rough_d * 0.5 or cw > rough_d * 1.8:
            continue  # width must look like a single bullet's diameter
        perimeter = cv2.arcLength(c, True)
        circularity = (4 * np.pi * area / (perimeter * perimeter)) if perimeter else 0
        candidates.append((x, y, cw, ch, area, circularity))

    if not candidates:
        return []

    # Calibrate this card's actual single-bullet height from the contours
    # that already look unambiguously round (clean, non-touching bullets),
    # instead of trusting the rough global guess.
    sure_singles = [ch for (_, _, cw, ch, _, circ) in candidates if circ >= 0.6 and 0.7 <= cw / ch <= 1.3]
    unit_h = float(np.median(sure_singles)) if sure_singles else rough_d

    boxes: list[BulletBox] = []
    for x, y, cw, ch, area, circularity in candidates:
        if ch <= unit_h * 1.2:
            # Looks like a single bullet: also require it to be roughly round.
            aspect = cw / ch if ch else 0
            if aspect < 0.55 or aspect > 1.8 or circularity < 0.45:
                continue
            boxes.append(BulletBox(x, y, cw, ch))
        else:
            # Consecutive clues with short text sit close enough that their
            # bullets visually touch and merge into one tall blob. Bullets on
            # a card all share the same diameter, so split the merged run
            # back into evenly-spaced same-size boxes instead of losing them
            # (height, not area, reveals the count, since the blob stays
            # bullet-width but grows bullet-height-tall per merged bullet).
            count = max(2, round(ch / unit_h))
            slice_h = ch / count
            for i in range(count):
                boxes.append(BulletBox(x, int(round(y + i * slice_h)), cw, int(round(slice_h))))

    boxes.sort(key=lambda b: b.cy)
    return boxes


def split_clue_regions(
    body_bgr: np.ndarray,
    bullets: list[BulletBox],
    top_margin: int = 4,
    bottom_safety_margin: int = 2,
    left_margin: int = 6,
    right_margin_fraction: float = 0.025,
) -> list[ClueRegion]:
    """Each region spans from just above its bullet to just above the next one.

    Horizontally, the crop starts right after the widest bullet (a single
    left edge shared by all 8 regions, since the bullets drift by only a few
    px across a card): leaving the bullet glyph in the crop made Tesseract
    read it as a stray leading character on every single clue. The right
    edge is similarly trimmed a little short of the card's own border, which
    otherwise shows up as a stray trailing character on short lines.
    """
    h, w = body_bgr.shape[:2]
    left = min(w - 1, max((b.x + b.w for b in bullets), default=0) + left_margin)
    right = max(left + 1, w - int(w * right_margin_fraction))
    regions: list[ClueRegion] = []
    for i, bullet in enumerate(bullets):
        top = max(0, bullet.y - top_margin)
        if i + 1 < len(bullets):
            bottom = max(top + 1, bullets[i + 1].y - bottom_safety_margin)
        else:
            bottom = h
        crop = body_bgr[top:bottom, left:right]
        regions.append(ClueRegion(index=i, top=top, bottom=bottom, image=crop))
    return regions


def extract_clue_regions(card_bgr: np.ndarray) -> tuple[np.ndarray, list[BulletBox], list[ClueRegion]]:
    body_top = find_body_top(card_bgr)
    body = card_bgr[body_top:, :]
    bullets = find_bullets(body)
    regions = split_clue_regions(body, bullets)
    return body, bullets, regions
