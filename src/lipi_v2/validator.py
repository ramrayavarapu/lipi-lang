"""Pre-execution validation for V2 runtime."""

import re

from .errors import V2LipiError
from .text_utils import is_escaped_quote


# Keep in sync with parser-supported block statements in parser.py.
BLOCK_STARTERS = ("if", "while")
BLOCK_MIDDLE = ("else:",)
BLOCK_END = "end"
UNSUPPORTED_TOKENS = ("exec(", "__import__(", "eval(")
_BLOCK_START_PATTERN_STR = rf"^({'|'.join(BLOCK_STARTERS)})(\b|\s|\()"
BLOCK_START_PATTERN = re.compile(_BLOCK_START_PATTERN_STR, flags=re.UNICODE)


def _contains_token_outside_strings(line: str, token: str) -> bool:
    in_string = False
    string_char = None
    i = 0
    while i < len(line):
        ch = line[i]
        if ch in {'"', "'"}:
            if not in_string:
                in_string = True
                string_char = ch
            elif string_char == ch and not is_escaped_quote(line, i):
                in_string = False
                string_char = None
            i += 1
            continue
        if not in_string and line.startswith(token, i):
            return True
        i += 1
    return False


def validate_normalized_lines(lines: list[str]) -> None:
    """Validate unsupported tokens and malformed block structure."""
    stack: list[str] = []

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        for token in UNSUPPORTED_TOKENS:
            if _contains_token_outside_strings(line, token):
                raise V2LipiError("unsupported_token", token, line=idx)

        if line.endswith(":") and BLOCK_START_PATTERN.match(line):
            stack.append(line)
            continue

        if line in BLOCK_MIDDLE:
            if not stack or not stack[-1].startswith("if "):
                raise V2LipiError("malformed_block", "else without matching if", line=idx)
            continue

        if line == BLOCK_END:
            if not stack:
                raise V2LipiError("malformed_block", "end without opening block", line=idx)
            stack.pop()

    if stack:
        raise V2LipiError("malformed_block", "missing end for block", line=len(lines))
