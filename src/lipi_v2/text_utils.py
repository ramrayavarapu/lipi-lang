"""Shared text parsing helpers for V2 runtime."""

import re
from collections.abc import Callable

# \u0C00-\u0C7F is Telugu Unicode block, allowing Telugu identifiers.
IDENTIFIER_PATTERN = re.compile(r"[_\w\u0C00-\u0C7F]+", flags=re.UNICODE)


def is_escaped_quote(text: str, quote_index: int) -> bool:
    """Return True when quote at index is escaped by odd backslashes."""
    slashes = 0
    j = quote_index - 1
    while j >= 0 and text[j] == "\\":
        slashes += 1
        j -= 1
    return slashes % 2 == 1


def transform_identifiers_outside_strings(text: str, transform: Callable[[str], str]) -> str:
    """Transform identifier tokens while preserving string literal contents."""
    out = []
    i = 0
    in_string = False
    string_char = None

    while i < len(text):
        ch = text[i]
        if ch in {'"', "'"}:
            if not in_string:
                in_string = True
                string_char = ch
            elif string_char == ch and not is_escaped_quote(text, i):
                in_string = False
                string_char = None
            out.append(ch)
            i += 1
            continue

        if in_string:
            out.append(ch)
            i += 1
            continue

        match = IDENTIFIER_PATTERN.match(text, i)
        if not match:
            out.append(ch)
            i += 1
            continue

        token = match.group(0)
        out.append(transform(token))
        i = match.end()

    return "".join(out)


def find_assignment_index(line: str) -> int:
    """Find standalone assignment '=' index outside strings and comparisons.

    Returns assignment index when found, otherwise -1.
    """
    in_string = False
    string_char = None
    for i, ch in enumerate(line):
        if ch in {'"', "'"}:
            if not in_string:
                in_string = True
                string_char = ch
            elif string_char == ch and not is_escaped_quote(line, i):
                in_string = False
                string_char = None
            continue
        if in_string:
            continue
        if ch == "=":
            prev_char = line[i - 1] if i > 0 else ""
            next_char = line[i + 1] if i + 1 < len(line) else ""
            if prev_char in {"<", ">", "!", "="} or next_char == "=":
                continue
            return i
    return -1
