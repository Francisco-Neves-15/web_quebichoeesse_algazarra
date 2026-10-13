"""Diagnostic tool: show OCR output for every pre-processing variant on one clue.

Usage:
    python compare_ocr.py <template-number 1-6> <dica-number 1-8>

Example:
    python compare_ocr.py 6 1
"""

from __future__ import annotations

import sys
from pathlib import Path

import cv2

from app import ocr, perspective, regions

ROOT = Path(__file__).resolve().parent
TEMPLATES_DIR = ROOT / "images-templates"


def main() -> None:
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    card_n = int(sys.argv[1])
    clue_n = int(sys.argv[2])

    image_path = TEMPLATES_DIR / f"card-fontsize-{card_n}.jpg"
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"Não encontrei {image_path}")
        sys.exit(1)

    quad = perspective.find_card_contour(img)
    warped = perspective.warp_card(img, quad)
    _body, _bullets, clue_regions = regions.extract_clue_regions(warped)

    if not (1 <= clue_n <= len(clue_regions)):
        print(f"Carta {card_n} tem {len(clue_regions)} dicas detectadas; dica {clue_n} fora do intervalo.")
        sys.exit(1)

    region = clue_regions[clue_n - 1]
    best, all_results = ocr.ocr_region_best(region.image)

    print(f"Carta {card_n}, Dica {clue_n}\n")
    for r in all_results:
        marker = " <= melhor" if r is best else ""
        conf_str = f"{r.confidence:5.1f}%" if r.confidence >= 0 else "  n/a "
        print(f"[{r.variant_name:18s}] conf={conf_str}  {r.text!r}{marker}")

    print(f"\nMelhor resultado ({best.variant_name}, conf={best.confidence:.1f}%):")
    print(best.text)


if __name__ == "__main__":
    main()
