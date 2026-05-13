"""Language normalizer for V2 pipeline."""

import re
from dataclasses import dataclass

from .dictionary import KEYWORD_MAP

IDENTIFIER_PATTERN = re.compile(r"[_\w\u0C00-\u0C7F]+", flags=re.UNICODE)


@dataclass
class NormalizationResult:
    normalized_lines: list[str]


def _replace_keywords(line: str, keyword_map: dict[str, str]) -> str:
    out = []
    i = 0
    in_string = False
    string_char = None

    while i < len(line):
        ch = line[i]
        if ch in {"\"", "'"}:
            if not in_string:
                in_string = True
                string_char = ch
            elif string_char == ch and not _is_escaped_quote(line, i):
                in_string = False
                string_char = None
            out.append(ch)
            i += 1
            continue

        if in_string:
            out.append(ch)
            i += 1
            continue

        match = IDENTIFIER_PATTERN.match(line, i)
        if not match:
            out.append(ch)
            i += 1
            continue

        token = match.group(0)
        out.append(keyword_map.get(token, token))
        i = match.end()

    return "".join(out)


def _is_escaped_quote(line: str, quote_index: int) -> bool:
    slashes = 0
    j = quote_index - 1
    while j >= 0 and line[j] == "\\":
        slashes += 1
        j -= 1
    return slashes % 2 == 1


def normalize_source(source: str, keyword_map: dict[str, str] | None = None) -> NormalizationResult:
    """Normalize Telugu/mixed source to canonical English-form keywords."""
    mapping = keyword_map or KEYWORD_MAP
    lines = source.splitlines()
    normalized = [_replace_keywords(line, mapping) for line in lines]
    return NormalizationResult(normalized_lines=normalized)
