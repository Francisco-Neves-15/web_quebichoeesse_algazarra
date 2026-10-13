"""Interactive terminal loop: pick a category, type name+index, "scan", review, confirm."""

from __future__ import annotations

import datetime as _dt
from pathlib import Path

import cv2

from app import exporter, ocr, parser, perspective, regions, validator

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = ROOT / "images-templates"
PROCESSED_DIR = ROOT / "data" / "processed"

CATEGORY_MENU: list[tuple[str, str]] = [
    ("mamiferos", "Mamíferos"),
    ("aves", "Aves"),
    ("repteis-anfibios-e-peixes", "Répteis, Anfíbios e Peixes"),
    ("invertebrados", "Invertebrados"),
    ("templates", "Templates (teste, sem câmera)"),
]

TEMPLATE_COUNT = 6


def _choose_category() -> str | None:
    print("\nCategorias:")
    for i, (_, label) in enumerate(CATEGORY_MENU, start=1):
        print(f"  {i}) {label}")
    print("  0) Sair")
    choice = input("Escolha: ").strip()
    if choice == "0":
        return None
    try:
        idx = int(choice) - 1
        if 0 <= idx < len(CATEGORY_MENU):
            return CATEGORY_MENU[idx][0]
    except ValueError:
        pass
    print("Opção inválida.")
    return _choose_category()


def _choose_template_image() -> Path | None:
    choice = input(f"'Escanear' -- escolha um template (1-{TEMPLATE_COUNT}, 0 para cancelar): ").strip()
    if choice == "0":
        return None
    try:
        n = int(choice)
        if 1 <= n <= TEMPLATE_COUNT:
            return TEMPLATES_DIR / f"card-fontsize-{n}.jpg"
    except ValueError:
        pass
    print("Opção inválida.")
    return _choose_template_image()


def _process_card(image_path: Path) -> tuple[list[ocr.OcrResult], Path, Path, list]:
    img = cv2.imread(str(image_path))
    if img is None:
        raise RuntimeError(f"Não foi possível ler a imagem: {image_path}")

    quad = perspective.find_card_contour(img)
    warped = perspective.warp_card(img, quad)
    body, bullets, clue_regions = regions.extract_clue_regions(warped)

    results = []
    for region in clue_regions:
        best, _all = ocr.ocr_region_best(region.image)
        results.append(best)

    return results, warped, body, clue_regions


def _save_debug(run_dir: Path, original_path: Path, warped, body, clue_regions) -> None:
    run_dir.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(run_dir / "00_original.jpg"), cv2.imread(str(original_path)))
    cv2.imwrite(str(run_dir / "01_warped.png"), warped)
    cv2.imwrite(str(run_dir / "02_body.png"), body)
    for region in clue_regions:
        cv2.imwrite(str(run_dir / f"03_dica_{region.index + 1:02d}.png"), region.image)


def _run_card_flow(category_key: str) -> None:
    print(f"\n-- Nova carta ({dict(CATEGORY_MENU)[category_key]}) --")
    animal_name = input("Nome do animal: ").strip()
    if not animal_name:
        print("Nome vazio, cancelado.")
        return
    try:
        animal_index = int(input("Índice (sortIndex): ").strip())
    except ValueError:
        print("Índice inválido, cancelado.")
        return

    image_path = _choose_template_image()
    if image_path is None:
        print("Cancelado.")
        return

    print("Processando...")
    try:
        results, warped, body, clue_regions = _process_card(image_path)
    except perspective.CardNotFoundError as e:
        print(f"Falha ao localizar a carta: {e}")
        return

    animal_code = parser.slugify_animal_name(animal_name)
    clue_warnings = validator.validate_clues(results)

    category_data = exporter.load_category(category_key)
    dup_warnings = validator.check_duplicate(category_data, animal_index, animal_code)
    all_warnings = clue_warnings + dup_warnings

    print(f"\nAnimal: {animal_name}  (animalCode={animal_code}, animalIndex={animal_index})")
    for i, r in enumerate(results, start=1):
        flag = " ⚠" if (r.confidence >= 0 and r.confidence < validator.LOW_CONFIDENCE_THRESHOLD) or not r.text.strip() else ""
        conf_str = f"{r.confidence:.0f}%" if r.confidence >= 0 else "?"
        print(f"  Dica {i} (conf={conf_str}, {r.variant_name}){flag}: {r.text}")

    if all_warnings:
        print("\nAvisos:")
        for w in all_warnings:
            print(f"  ⚠ {w.message}")

    answer = input("\nDigite 'c' e Enter para confirmar (qualquer outra tecla cancela): ").strip().lower()
    if answer != "c":
        print("Cancelado, carta não foi salva.")
        return

    clues = [r.text for r in results]
    path = exporter.append_entry(category_key, animal_index, animal_code, animal_name, clues)

    timestamp = _dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = PROCESSED_DIR / category_key / f"{animal_code}_{timestamp}"
    _save_debug(run_dir, image_path, warped, body, clue_regions)

    print(f"Salvo em {path}")
    print(f"Imagens de diagnóstico em {run_dir}")


def run() -> None:
    print("Card Scanner OCR -- prova de conceito (fase templates)")
    while True:
        category_key = _choose_category()
        if category_key is None:
            print("Até mais.")
            return
        while True:
            _run_card_flow(category_key)
            again = input("\nOutra carta nesta categoria? (s/n): ").strip().lower()
            if again != "s":
                break
