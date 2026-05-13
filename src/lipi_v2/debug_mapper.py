"""Source/AST mapping for V2 debugging."""

from dataclasses import dataclass


@dataclass
class SourceMapEntry:
    line_no: int
    original_line: str
    normalized_line: str
    ast_node_id: str | None = None


class DebugMapper:
    """Tracks Original ↔ Normalized ↔ AST mapping."""

    def __init__(self):
        self.entries: dict[int, SourceMapEntry] = {}
        self.node_to_line: dict[str, int] = {}

    def record_normalization(self, line_no: int, original: str, normalized: str) -> None:
        self.entries[line_no] = SourceMapEntry(
            line_no=line_no,
            original_line=original,
            normalized_line=normalized,
        )

    def bind_node(self, line_no: int, node_id: str) -> None:
        if line_no in self.entries:
            self.entries[line_no].ast_node_id = node_id
        self.node_to_line[node_id] = line_no

    def original_line(self, line_no: int) -> str:
        return self.entries.get(line_no, SourceMapEntry(line_no, "", "")).original_line
