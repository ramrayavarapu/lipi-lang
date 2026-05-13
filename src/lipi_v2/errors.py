"""V2 runtime error types."""

from dataclasses import dataclass


@dataclass
class V2LipiError(Exception):
    """Structured V2 error with taxonomy key."""

    key: str
    detail: str = ""
    line: int | None = None

    def __str__(self) -> str:
        location = f" (line {self.line})" if self.line is not None else ""
        return f"{self.key}{location}: {self.detail}" if self.detail else f"{self.key}{location}"
