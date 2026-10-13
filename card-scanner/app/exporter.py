"""Read/write the category JSON files under data/output/."""

from __future__ import annotations

import json
from pathlib import Path

CATEGORY_FILES: dict[str, str] = {
    "mamiferos": "mamiferos.json",
    "aves": "aves.json",
    "repteis-anfibios-e-peixes": "repteis-anfibios-e-peixes.json",
    "invertebrados": "invertebrados.json",
    "templates": "templates.json",
}

DATA_OUTPUT_DIR = Path(__file__).resolve().parent.parent / "data" / "output"


def category_path(category_key: str) -> Path:
    return DATA_OUTPUT_DIR / CATEGORY_FILES[category_key]


def load_category(category_key: str) -> dict:
    path = category_path(category_key)
    return json.loads(path.read_text(encoding="utf-8"))


def _is_placeholder(animal: dict) -> bool:
    return (
        animal.get("animalIndex") == 0
        and animal.get("animalCode") == ""
        and animal.get("animalName") == ""
        and animal.get("clues") == []
    )


def append_entry(category_key: str, animal_index: int, animal_code: str, animal_name: str, clues: list[str]) -> Path:
    """Append one animal entry, replacing the untouched placeholder if present.

    Never touches categorieCode / categorieShortCode / categorieName.
    """
    path = category_path(category_key)
    data = load_category(category_key)

    entry = {
        "animalIndex": animal_index,
        "animalCode": animal_code,
        "animalName": animal_name,
        "clues": clues,
    }

    animals = data.get("animals", [])
    if len(animals) == 1 and _is_placeholder(animals[0]):
        data["animals"] = [entry]
    else:
        animals.append(entry)
        data["animals"] = animals

    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return path
