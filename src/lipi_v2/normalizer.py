"""Language normalizer for V2 pipeline."""

from dataclasses import dataclass

from .dictionary import KEYWORD_MAP
from .text_utils import transform_identifiers_outside_strings

@dataclass
class NormalizationResult:
    normalized_lines: list[str]


def _replace_keywords(line: str, keyword_map: dict[str, str]) -> str:
    return transform_identifiers_outside_strings(line, lambda token: keyword_map.get(token, token))


def normalize_source(source: str, keyword_map: dict[str, str] | None = None) -> NormalizationResult:
    """Normalize Telugu/mixed source to canonical English-form keywords."""
    mapping = keyword_map or KEYWORD_MAP
    lines = source.splitlines()
    normalized = [_replace_keywords(line, mapping) for line in lines]
    return NormalizationResult(normalized_lines=normalized)
