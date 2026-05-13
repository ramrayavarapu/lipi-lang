"""Pre-execution validation for V2 runtime."""

import re

from .errors import V2LipiError


BLOCK_STARTERS = ("if", "while", "function", "for")
BLOCK_MIDDLE = ("else:",)
BLOCK_END = "end"
UNSUPPORTED_TOKENS = ("exec(", "__import__(", "eval(")
BLOCK_START_PATTERN = re.compile(rf"^({'|'.join(BLOCK_STARTERS)})(\b|\s|\()", flags=re.UNICODE)


def validate_normalized_lines(lines: list[str]) -> None:
    """Validate unsupported tokens and malformed block structure."""
    stack: list[str] = []

    for idx, raw in enumerate(lines, start=1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue

        for token in UNSUPPORTED_TOKENS:
            if token in line:
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
