"""AST node model for V2 runtime."""

from dataclasses import dataclass, field


@dataclass
class Node:
    line: int
    node_id: str = field(default="")


@dataclass
class Program(Node):
    statements: list[Node] = field(default_factory=list)


@dataclass
class Expr(Node):
    pass


@dataclass
class Literal(Expr):
    value: int | float | str | bool | None = None


@dataclass
class Variable(Expr):
    name: str = ""


@dataclass
class BinaryOp(Expr):
    left: Expr = None
    op: str = ""
    right: Expr = None


@dataclass
class Compare(Expr):
    left: Expr = None
    op: str = ""
    right: Expr = None


@dataclass
class Call(Expr):
    name: str = ""
    args: list[Expr] = field(default_factory=list)


@dataclass
class Assignment(Node):
    name: str = ""
    expr: Expr = None


@dataclass
class Print(Node):
    expr: Expr = None


@dataclass
class If(Node):
    condition: Expr = None
    then_body: list[Node] = field(default_factory=list)
    else_body: list[Node] = field(default_factory=list)


@dataclass
class While(Node):
    condition: Expr = None
    body: list[Node] = field(default_factory=list)


@dataclass
class ExprStmt(Node):
    expr: Expr = None
