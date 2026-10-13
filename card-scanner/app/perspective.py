"""Card localization and perspective correction.

The cards are photographed on a dark red fabric background. Empirically
(sampled directly from the template images) the background is reddish and
dark (red channel clearly above green, low brightness), while the card body
is bright and desaturated and the card header is green (green channel
clearly above red and blue). That contrast is enough to separate "card" from
"background" without assuming any fixed card size or orientation.
"""

from __future__ import annotations

import cv2
import numpy as np


class CardNotFoundError(RuntimeError):
    pass


def _background_mask(image_bgr: np.ndarray) -> np.ndarray:
    b = image_bgr[:, :, 0].astype(np.int16)
    g = image_bgr[:, :, 1].astype(np.int16)
    r = image_bgr[:, :, 2].astype(np.int16)
    value = np.maximum(np.maximum(b, g), r)
    is_reddish = (r - g) > 15
    is_dark = value < 120
    return (is_reddish & is_dark).astype(np.uint8) * 255


def find_card_contour(image_bgr: np.ndarray, min_area_ratio: float = 0.1) -> np.ndarray:
    """Return the 4 corner points (float32, tl/tr/br/bl) of the largest card-like blob."""
    h, w = image_bgr.shape[:2]
    bg_mask = _background_mask(image_bgr)
    fg_mask = cv2.bitwise_not(bg_mask)

    # Kept deliberately small: several sample photos only show a thin sliver
    # of background around the card (or none at all, when a second card is
    # visible behind it). A large kernel bridges that sliver away and makes
    # the whole frame look like one blob, so err on the side of a gentle
    # cleanup that only removes fabric-texture speckle noise.
    open_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    close_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_OPEN, open_kernel)
    fg_mask = cv2.morphologyEx(fg_mask, cv2.MORPH_CLOSE, close_kernel)

    contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        raise CardNotFoundError("Nenhum contorno encontrado separando a carta do fundo.")

    image_area = float(h * w)
    candidates = [c for c in contours if cv2.contourArea(c) >= image_area * min_area_ratio]
    if not candidates:
        raise CardNotFoundError("Nenhum contorno grande o suficiente para ser a carta.")

    card_contour = max(candidates, key=cv2.contourArea)
    rect = cv2.minAreaRect(card_contour)
    box = cv2.boxPoints(rect)
    return _order_points(box)


def _order_points(points: np.ndarray) -> np.ndarray:
    pts = points.astype(np.float32)
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1).reshape(-1)
    ordered = np.zeros((4, 2), dtype=np.float32)
    ordered[0] = pts[np.argmin(s)]  # top-left
    ordered[2] = pts[np.argmax(s)]  # bottom-right
    ordered[1] = pts[np.argmin(diff)]  # top-right
    ordered[3] = pts[np.argmax(diff)]  # bottom-left
    return ordered


def warp_card(image_bgr: np.ndarray, quad: np.ndarray) -> np.ndarray:
    """Perspective-warp the quad to its own measured width/height (no fixed canonical size)."""
    tl, tr, br, bl = quad
    width = int(round(max(np.linalg.norm(tr - tl), np.linalg.norm(br - bl))))
    height = int(round(max(np.linalg.norm(bl - tl), np.linalg.norm(br - tr))))
    width = max(width, 10)
    height = max(height, 10)

    dst = np.array(
        [[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]],
        dtype=np.float32,
    )
    matrix = cv2.getPerspectiveTransform(quad, dst)
    warped = cv2.warpPerspective(image_bgr, matrix, (width, height))

    # The card may have been detected sideways (minAreaRect has no inherent
    # "up"); the header (dark, low-brightness band) should end up on top.
    # Compare the mean brightness of the top vs bottom 20% band and rotate
    # 180 degrees if the header looks like it landed on the bottom.
    band = max(1, height // 5)
    top_v = cv2.cvtColor(warped[:band, :], cv2.COLOR_BGR2GRAY).mean()
    bottom_v = cv2.cvtColor(warped[-band:, :], cv2.COLOR_BGR2GRAY).mean()
    if top_v > bottom_v:
        warped = cv2.rotate(warped, cv2.ROTATE_180)

    return warped


def detect_and_warp(image_bgr: np.ndarray) -> np.ndarray:
    quad = find_card_contour(image_bgr)
    return warp_card(image_bgr, quad)
