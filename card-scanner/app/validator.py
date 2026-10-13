"""Advisory checks shown to the user before they confirm a scanned card.

Nothing here blocks saving -- the human review ("c" to confirm) is the real
gate, per the brief. This only decides what gets a warning icon.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.ocr import OcrResult

LOW_CONFIDENCE_THRESHOLD = 60.0
MIN_CLUE_LENGTH = 4


@dataclass
class Warning_:
    message: str


def validate_clues(results: list[OcrResult]) -> list[Warning_]:
    warnings: list[Warning_] = []

    if len(results) != 8:
        warnings.append(Warning_(f"esperado 8 dicas, encontradas {len(results)}"))

    for i, r in enumerate(results, start=1):
        if not r.text.strip():
            warnings.append(Warning_(f"dica {i}: vazia"))
            continue
        if len(r.text.strip()) < MIN_CLUE_LENGTH:
            warnings.append(Warning_(f"dica {i}: texto muito curto ({r.text!r})"))
        if 0 <= r.confidence < LOW_CONFIDENCE_THRESHOLD:
            warnings.append(Warning_(f"dica {i}: confiança baixa ({r.confidence:.0f}%)"))

    return warnings


def check_duplicate(category: dict, animal_index: int, animal_code: str) -> list[Warning_]:
    warnings: list[Warning_] = []
    for animal in category.get("animals", []):
        if animal.get("animalCode") == "" and animal.get("animalName") == "":
            continue  # the untouched placeholder entry
        if animal.get("animalIndex") == animal_index:
            warnings.append(Warning_(f"já existe um animal com animalIndex={animal_index} ({animal.get('animalName')!r})"))
        if animal.get("animalCode") == animal_code:
            warnings.append(Warning_(f"já existe um animal com animalCode={animal_code!r}"))
    return warnings
