"""Generate several candidate pre-processings for a single clue region.

Font size (and therefore effective resolution) varies from card to card, so
instead of picking one fixed pipeline we produce a handful of named variants
at different scales/techniques and let the OCR step (app/ocr.py) score them
empirically and keep the best one. This mirrors Etapa 2 of the brief: do not
assume a single pre-processing works for every card.
"""

from __future__ import annotations

import cv2
import numpy as np

Variant = tuple[str, np.ndarray]


def _upscale(gray: np.ndarray, factor: float) -> np.ndarray:
    if factor == 1:
        return gray
    return cv2.resize(gray, None, fx=factor, fy=factor, interpolation=cv2.INTER_CUBIC)


def _clahe(gray: np.ndarray) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    return clahe.apply(gray)


def _sharpen(gray: np.ndarray) -> np.ndarray:
    blurred = cv2.GaussianBlur(gray, (0, 0), sigmaX=2)
    return cv2.addWeighted(gray, 1.6, blurred, -0.6, 0)


def generate_variants(region_bgr: np.ndarray) -> list[Variant]:
    gray = cv2.cvtColor(region_bgr, cv2.COLOR_BGR2GRAY)

    variants: list[Variant] = []
    for scale in (2, 3):
        up = _upscale(gray, scale)

        variants.append((f"gray_{scale}x", up))

        _, otsu = cv2.threshold(up, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        variants.append((f"otsu_{scale}x", otsu))

        adaptive = cv2.adaptiveThreshold(
            up, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
        )
        variants.append((f"adaptive_{scale}x", adaptive))

        clahe_img = _clahe(up)
        _, clahe_otsu = cv2.threshold(clahe_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        variants.append((f"clahe_otsu_{scale}x", clahe_otsu))

        sharpened = _sharpen(up)
        _, sharp_otsu = cv2.threshold(sharpened, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        variants.append((f"sharpen_otsu_{scale}x", sharp_otsu))

    denoised = cv2.fastNlMeansDenoising(_upscale(gray, 3), h=10)
    _, denoise_otsu = cv2.threshold(denoised, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    variants.append(("denoise_otsu_3x", denoise_otsu))

    return variants
