"""AST execution engine for V2 runtime."""

import os

from .ast_nodes import Assignment, BinaryOp, Call, Compare, ExprStmt, If, Literal, Print, Program, Variable, While
from .errors import V2LipiError

# Guardrail for runaway while-loops in the interpreter.
# 100000 was chosen as a high default that permits normal workloads while
# preventing accidental non-terminating loops from hanging execution.
# Can be overridden with LIPI_V2_MAX_LOOP_ITERATIONS.
MAX_LOOP_ITERATIONS = int(os.getenv("LIPI_V2_MAX_LOOP_ITERATIONS", "100000"))


class ExecutionEngine:
    """Language-neutral AST interpreter."""

    def __init__(self):
        self.env: dict[str, object] = {}

    def execute(self, program: Program) -> dict[str, object]:
        for stmt in program.statements:
            self._exec_stmt(stmt)
        return self.env

    def _exec_stmt(self, stmt):
        if isinstance(stmt, Assignment):
            self.env[stmt.name] = self._eval_expr(stmt.expr)
            return

        if isinstance(stmt, Print):
            print(self._eval_expr(stmt.expr))
            return

        if isinstance(stmt, If):
            if self._truthy(self._eval_expr(stmt.condition)):
                for inner in stmt.then_body:
                    self._exec_stmt(inner)
            else:
                for inner in stmt.else_body:
                    self._exec_stmt(inner)
            return

        if isinstance(stmt, While):
            safety_counter = 0
            while self._truthy(self._eval_expr(stmt.condition)):
                safety_counter += 1
                if safety_counter > MAX_LOOP_ITERATIONS:
                    raise V2LipiError("runtime_error", "loop safety limit exceeded", line=stmt.line)
                for inner in stmt.body:
                    self._exec_stmt(inner)
            return

        if isinstance(stmt, ExprStmt):
            self._eval_expr(stmt.expr)
            return

        raise V2LipiError("runtime_error", f"unsupported statement {type(stmt).__name__}", line=getattr(stmt, "line", None))

    def _truthy(self, value):
        return bool(value)

    def _eval_expr(self, expr):
        if isinstance(expr, Literal):
            return expr.value

        if isinstance(expr, Variable):
            if expr.name not in self.env:
                raise V2LipiError("variable_not_defined", expr.name, line=expr.line)
            return self.env[expr.name]

        if isinstance(expr, BinaryOp):
            left = self._eval_expr(expr.left)
            right = self._eval_expr(expr.right)
            return self._binary(left, right, expr.op, expr.line)

        if isinstance(expr, Compare):
            left = self._eval_expr(expr.left)
            right = self._eval_expr(expr.right)
            return self._compare(left, right, expr.op)

        if isinstance(expr, Call):
            if expr.name == "len" and len(expr.args) == 1:
                return len(self._eval_expr(expr.args[0]))
            raise V2LipiError("runtime_error", f"unsupported call: {expr.name}", line=expr.line)

        raise V2LipiError("runtime_error", f"unsupported expression {type(expr).__name__}", line=getattr(expr, "line", None))

    def _binary(self, left, right, op, line):
        if op == "Add":
            return left + right
        if op == "Sub":
            return left - right
        if op == "Mult":
            return left * right
        if op == "Div":
            if isinstance(right, (int, float)) and right == 0:
                raise V2LipiError("runtime_error", "division by zero", line=line)
            return left / right
        if op == "Mod":
            return left % right
        if op == "Pow":
            return left ** right
        raise V2LipiError("type_error", f"unsupported binary op: {op}", line=line)

    def _compare(self, left, right, op):
        if op == "Eq":
            return left == right
        if op == "NotEq":
            return left != right
        if op == "Gt":
            return left > right
        if op == "Lt":
            return left < right
        if op == "GtE":
            return left >= right
        if op == "LtE":
            return left <= right
        raise V2LipiError("type_error", f"unsupported compare op: {op}")
