"""Tesseract wrapper: run every preprocessing variant and keep the best one."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pytesseract

from app.preprocessing import generate_variants

_NOISE_TOKEN_RE = re.compile(r"^[|=+_~°»«“”\"'`^]+$")

_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "ocr.json"
_configured = False


@dataclass
class OcrResult:
    text: str
    confidence: float  # 0-100, mean of per-word confidences (-1 if no words)
    variant_name: str


def _ensure_configured() -> dict:
    global _configured
    cfg = json.loads(_CONFIG_PATH.read_text(encoding="utf-8"))
    if not _configured:
        pytesseract.pytesseract.tesseract_cmd = cfg["tesseract_cmd"]
        _configured = True
    return cfg


def _ocr_image(image: np.ndarray, lang: str, psm: int, oem: int) -> OcrResult:
    config = f"--oem {oem} --psm {psm}"
    data = pytesseract.image_to_data(
        image, lang=lang, config=config, output_type=pytesseract.Output.DICT
    )
    words = []
    confidences = []
    for text, conf in zip(data["text"], data["conf"]):
        text = text.strip()
        conf = float(conf)
        if text and conf >= 0:
            words.append(text)
            confidences.append(conf)
    # Crop edges (bullet glyph, card border) occasionally leave a stray
    # symbol-only token dangling at either end (e.g. "|", "+"); trim it
    # deterministically rather than passing it on for the human to retype.
    while words and _NOISE_TOKEN_RE.match(words[-1]):
        words.pop()
    while words and _NOISE_TOKEN_RE.match(words[0]):
        words.pop(0)

    joined = " ".join(words)
    mean_conf = sum(confidences) / len(confidences) if confidences else -1.0
    return OcrResult(text=joined, confidence=mean_conf, variant_name="")


def ocr_region_best(region_bgr: np.ndarray) -> tuple[OcrResult, list[OcrResult]]:
    """Run every pre-processing variant and return (best, all_results)."""
    cfg = _ensure_configured()
    lang, psm, oem = cfg["lang"], cfg["psm"], cfg["oem"]

    results: list[OcrResult] = []
    for name, variant_img in generate_variants(region_bgr):
        result = _ocr_image(variant_img, lang=lang, psm=psm, oem=oem)
        result.variant_name = name
        results.append(result)

    non_empty = [r for r in results if r.text]
    if non_empty:
        best = max(non_empty, key=lambda r: r.confidence)
    else:
        best = results[0] if results else OcrResult(text="", confidence=-1.0, variant_name="none")
    return best, results
