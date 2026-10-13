"""Deterministic animalCode slug generation from a manually-typed animal name."""

from __future__ import annotations

import re
import unicodedata

_PAREN_RE = re.compile(r"^(.*?)\s*\((.*)\)\s*$")


def _strip_accents(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def _convert_segment(segment: str) -> str:
    segment = re.sub(r"\s+", " ", segment.strip())
    segment = segment.replace("-", "--")
    segment = segment.replace(" ", "-")
    return segment


def slugify_animal_name(name: str) -> str:
    """animalCode rules (confirmed with the user):

    - lowercase, accents stripped;
    - a space between words becomes a single hyphen ("-");
    - an existing hyphen becomes a double hyphen ("--");
    - a trailing "(...)" is wrapped in triple hyphens: " (" becomes "---"
      and the closing ")" becomes "---", with the same space/hyphen rules
      applied inside the parentheses.

    Examples: "Cavalo-Marinho" -> "cavalo--marinho";
    "dragão-de-komodo (varanus komodoensis)" ->
    "dragao--de--komodo---varanus-komodoensis---";
    "Tubarão Branco" -> "tubarao-branco".
    """
    normalized = _strip_accents(name).lower().strip()

    match = _PAREN_RE.match(normalized)
    if match:
        main, paren = match.groups()
        return f"{_convert_segment(main)}---{_convert_segment(paren)}---"
    return _convert_segment(normalized)
