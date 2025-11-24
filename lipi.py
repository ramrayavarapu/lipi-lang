#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lipi Language - v0.1
A minimal Telugu-first scripting language.

Supported:
- Variable assignment:  పేరు = "రామ్",  వయసు = 10
- Integer + operator:   మొత్తం = వయసు + 5
- Print:                చెప్పు "నమస్తే", చెప్పు పేరు
- Comments:             # this is a comment

Usage:
    python lipi.py examples/hello.lipi
    (or run without args for a simple REPL)
    More code to come in future versions!
"""

import sys

def eval_lipi_expr(expr, env):
    """
    Evaluate a simple Lipi expression.
    Supported:
    - String literals: "text"
    - Integer literals: 10
    - Binary + : a + b  (string concat OR numeric add)
    - Variables: పేరు, వయసు, etc.
    """
    expr = expr.strip()

    # String literal
    if (expr.startswith('"') and expr.endswith('"')) or \
       (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]

    # Integer literal
    try:
        return int(expr)
    except ValueError:
        pass

    # Binary plus: support a single "a + b" for v0.1
    if " + " in expr:
        left, right = expr.split(" + ", 1)
        left_val = eval_lipi_expr(left, env)
        right_val = eval_lipi_expr(right, env)

        # If either side is a string → string concatenation
        if isinstance(left_val, str) or isinstance(right_val, str):
            return str(left_val) + str(right_val)

        # Otherwise numeric addition
        return left_val + right_val

    # Comparisons
    for op in [">=", "<=", "==", "!=", ">", "<"]:
        if op in expr:
            left, right = expr.split(op, 1)
            left_val = eval_lipi_expr(left, env)
            right_val = eval_lipi_expr(right, env)

            if op == ">":  return left_val > right_val
            if op == "<":  return left_val < right_val
            if op == ">=": return left_val >= right_val
            if op == "<=": return left_val <= right_val
            if op == "==": return left_val == right_val
            if op == "!=": return left_val != right_val


    # Variable lookup
    if expr in env:
        return env[expr]

    raise ValueError(f"తెలియని వ్యక్తీకరణ (unknown expression): {expr}")

def run_lipi_block(lines, start_index, env):
    """
    Processes an IF/ELSE block starting at start_index.
    Returns next index to continue execution.
    """

    line = lines[start_index].strip()

    # --- IF START ---
    if line.startswith("యెడల ") and line.endswith(":"):
        condition_expr = line[len("యెడల "):-1].strip()

        # Evaluate condition (true/false)
        condition_value = eval_lipi_expr(condition_expr, env)
        condition_true = bool(condition_value)

        # Collect IF body
        if_body = []
        else_body = []
        current = if_body

        i = start_index + 1
        while i < len(lines):
            stripped = lines[i].strip()

            if stripped == "లేకపోతే:":
                current = else_body
                i += 1
                continue

            if stripped == "ముగింపు":
                break

            current.append(stripped)
            i += 1

        # Execute correct block
        body_to_run = if_body if condition_true else else_body
        for statement in body_to_run:
            run_lipi_line(statement, env)

        # return index just after ముగింపు
        return i + 1

    # NOT an if-block
    return start_index

def run_lipi_file(path):
    env = {}

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if not line or line.startswith("#"):
            i += 1
            continue

        # IF BLOCK DETECTED
        if line.startswith("యెడల ") and line.endswith(":"):
            i = run_lipi_block(lines, i, env)
            continue

        # Standard single-line statement
        try:
            run_lipi_line(line, env)
        except Exception as e:
            print(f"[లోపం] లైన్ {i+1}: {e}")
            break

        i += 1

def run_lipi_line(line, env):
    """
    Execute a single line of Lipi code.
    """
    line = line.strip()

    # Empty / comment
    if not line or line.startswith("#"):
        return

    # Print statement: చెప్పు expr
    if line.startswith("చెప్పు "):
        expr = line[len("చెప్పు "):]
        value = eval_lipi_expr(expr, env)
        print(value)
        return

    # Assignment: name = expr
    if "=" in line:
        name, expr = line.split("=", 1)
        name = name.strip()
        expr = expr.strip()
        env[name] = eval_lipi_expr(expr, env)
        return

    # If we reach here, syntax is unknown for v0.1
    raise SyntaxError(f"తెలియని లైన్ (unknown line): {line}")


def run_lipi_file(path):
    env = {}
    with open(path, "r", encoding="utf-8") as f:
        for lineno, raw_line in enumerate(f, start=1):
            line = raw_line.rstrip("\n")
            try:
                run_lipi_line(line, env)
            except Exception as e:
                print(f"[లోపం] లైన్ {lineno}: {e}")
                break


def repl():
    """
    Simple interactive shell for Lipi.
    """
    print("Lipi v0.1 REPL – తెలుగు లో కోడ్ రాయండి (type Ctrl+C to exit)")
    env = {}
    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nవీడ్కోలు! (Goodbye!)")
            break

        try:
            run_lipi_line(line, env)
        except Exception as e:
            print(f"[లోపం] {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_lipi_file(sys.argv[1])
    else:
        repl()
