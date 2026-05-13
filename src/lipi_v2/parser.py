"""Parser for normalized V2 source -> AST."""

import ast as pyast

from .ast_nodes import (
    Assignment,
    BinaryOp,
    Call,
    Compare,
    ExprStmt,
    If,
    Literal,
    Print,
    Program,
    Variable,
    While,
)
from .errors import V2LipiError


class Parser:
    """Line-based parser for V2 normalized source."""

    def __init__(self, debug_mapper=None):
        self.debug_mapper = debug_mapper
        self._counter = 0

    def _next_id(self) -> str:
        self._counter += 1
        return f"n{self._counter}"

    def parse(self, lines: list[str]) -> Program:
        statements, idx = self._parse_block(lines, 0)
        if idx != len(lines):
            raise V2LipiError("parser_error", "unexpected trailing tokens", line=idx + 1)
        program = Program(line=1, statements=statements)
        program.node_id = self._next_id()
        return program

    def _parse_block(self, lines: list[str], start: int, stop_tokens: tuple[str, ...] = ()) -> tuple[list, int]:
        out = []
        i = start
        while i < len(lines):
            raw = lines[i]
            line = raw.strip()
            if not line or line.startswith("#"):
                i += 1
                continue

            if stop_tokens and line in stop_tokens:
                return out, i

            stmt, i = self._parse_statement(lines, i)
            out.append(stmt)

        return out, i

    def _bind(self, node, line_no: int):
        node.node_id = self._next_id()
        if self.debug_mapper:
            self.debug_mapper.bind_node(line_no, node.node_id)
        return node

    def _parse_statement(self, lines: list[str], i: int):
        line_no = i + 1
        line = lines[i].strip()

        if line.startswith("if ") and line.endswith(":"):
            condition = self._parse_expr(line[3:-1].strip(), line_no)
            then_body, j = self._parse_block(lines, i + 1, stop_tokens=("else:", "end"))
            else_body = []
            if j < len(lines) and lines[j].strip() == "else:":
                else_body, j = self._parse_block(lines, j + 1, stop_tokens=("end",))
            if j >= len(lines) or lines[j].strip() != "end":
                raise V2LipiError("parser_error", "if block missing end", line=line_no)
            return self._bind(If(line=line_no, condition=condition, then_body=then_body, else_body=else_body), line_no), j + 1

        if line.startswith("while ") and line.endswith(":"):
            condition = self._parse_expr(line[6:-1].strip(), line_no)
            body, j = self._parse_block(lines, i + 1, stop_tokens=("end",))
            if j >= len(lines) or lines[j].strip() != "end":
                raise V2LipiError("parser_error", "while block missing end", line=line_no)
            return self._bind(While(line=line_no, condition=condition, body=body), line_no), j + 1

        if line.startswith("print "):
            expr = self._parse_expr(line[len("print "):].strip(), line_no)
            return self._bind(Print(line=line_no, expr=expr), line_no), i + 1

        if line.startswith("call "):
            expr = self._parse_expr(line[len("call "):].strip(), line_no)
            return self._bind(ExprStmt(line=line_no, expr=expr), line_no), i + 1

        if "=" in line and not any(op in line for op in ["==", "!=", ">=", "<="]):
            name, expr = line.split("=", 1)
            node = Assignment(line=line_no, name=name.strip(), expr=self._parse_expr(expr.strip(), line_no))
            return self._bind(node, line_no), i + 1

        # Fallback expression statement
        return self._bind(ExprStmt(line=line_no, expr=self._parse_expr(line, line_no)), line_no), i + 1

    def _parse_expr(self, expr: str, line_no: int):
        pythonish = (
            expr.replace(" true", " True")
            .replace(" false", " False")
            .replace(" null", " None")
        )
        pythonish = pythonish.replace("true", "True").replace("false", "False").replace("null", "None")
        try:
            node = pyast.parse(pythonish, mode="eval").body
            return self._convert_expr(node, line_no)
        except V2LipiError:
            raise
        except Exception as exc:
            raise V2LipiError("parser_error", str(exc), line=line_no) from exc

    def _convert_expr(self, node, line_no: int):
        if isinstance(node, pyast.Constant):
            return Literal(line=line_no, value=node.value)
        if isinstance(node, pyast.Name):
            return Variable(line=line_no, name=node.id)
        if isinstance(node, pyast.BinOp):
            return BinaryOp(
                line=line_no,
                left=self._convert_expr(node.left, line_no),
                op=type(node.op).__name__,
                right=self._convert_expr(node.right, line_no),
            )
        if isinstance(node, pyast.Compare) and len(node.ops) == 1 and len(node.comparators) == 1:
            return Compare(
                line=line_no,
                left=self._convert_expr(node.left, line_no),
                op=type(node.ops[0]).__name__,
                right=self._convert_expr(node.comparators[0], line_no),
            )
        if isinstance(node, pyast.Call) and isinstance(node.func, pyast.Name):
            return Call(
                line=line_no,
                name=node.func.id,
                args=[self._convert_expr(arg, line_no) for arg in node.args],
            )

        raise V2LipiError("parser_error", f"unsupported expression", line=line_no)
