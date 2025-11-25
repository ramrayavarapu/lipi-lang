#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lipi Language - v0.3
A minimal Telugu-first scripting language.

Supported:
- Variable assignment:  పేరు = "రామ్",  వయసు = 10
- Integer + operator:   మొత్తం = వయసు + 5
- String concat:        "వయసు: " + వయసు
- Print:                చెప్పు "నమస్తే", చెప్పు పేరు
- Comments:             # this is a comment
- If/else blocks:

    యెడల వయసు > 18:
        చెప్పు "అడల్ట్"
    లేకపోతే:
        చెప్పు "యంగ్"
    ముగింపు

- While loops:

    వరకు వయసు < 21:
        చెప్పు "వయసు: " + వయసు
        వయసు = వయసు + 1
    ముగింపు
"""

import sys


# ---------------------------
# Expression evaluator
# ---------------------------
def eval_lipi_expr(expr, env):
    """
    Evaluate a simple Lipi expression.
    Supported:
    - String literals: "text"
    - Integer literals: 10
    - Binary + : a + b  (string concat OR numeric add)
    - Comparisons: >, <, >=, <=, ==, !=
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

    # Comparisons
    for op in [">=", "<=", "==", "!=", ">", "<"]:
        if op in expr:
            left, right = expr.split(op, 1)
            left_val = eval_lipi_expr(left, env)
            right_val = eval_lipi_expr(right, env)

            if op == ">":
                return left_val > right_val
            if op == "<":
                return left_val < right_val
            if op == ">=":
                return left_val >= right_val
            if op == "<=":
                return left_val <= right_val
            if op == "==":
                return left_val == right_val
            if op == "!=":
                return left_val != right_val

    # Binary plus: support a single "a + b" for v0.x
    if " + " in expr:
        left, right = expr.split(" + ", 1)
        left_val = eval_lipi_expr(left, env)
        right_val = eval_lipi_expr(right, env)

        # If either side is a string → string concatenation
        if isinstance(left_val, str) or isinstance(right_val, str):
            return str(left_val) + str(right_val)

        # Otherwise numeric addition
        return left_val + right_val

    # Variable lookup
    if expr in env:
        return env[expr]

    raise ValueError(f"తెలియని వ్యక్తీకరణ (unknown expression): {expr}")


# ---------------------------
# Single-line executor
# ---------------------------
def run_lipi_line(line, env):
    """
    Execute a single line of Lipi code (non-block).
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

    # If we reach here, syntax is unknown for v0.3 (outside blocks)
    raise SyntaxError(f"తెలియని లైన్ (unknown line): {line}")


# ---------------------------
# Block executor (if/else)
# ---------------------------
def run_lipi_if_block(lines, start_index, env):
    """
    Processes an IF/ELSE block starting at start_index.
    Returns next index to continue execution.
    """

    line = lines[start_index].strip()

    if not (line.startswith("యెడల ") and line.endswith(":")):
        return start_index

    condition_expr = line[len("యెడల "):-1].strip()

    # Evaluate condition (true/false)
    condition_value = eval_lipi_expr(condition_expr, env)
    condition_true = bool(condition_value)

    # Collect IF and ELSE bodies
    if_body = []
    else_body = []
    current = if_body

    i = start_index + 1
    while i < len(lines):
        stripped = lines[i].strip()

        # ELSE branch
        if stripped == "లేకపోతే:":
            current = else_body
            i += 1
            continue

        # END of block
        if stripped == "ముగింపు":
            break

        current.append(stripped)
        i += 1

    # Execute chosen body
    body_to_run = if_body if condition_true else else_body
    for statement in body_to_run:
        run_lipi_line(statement, env)

    # Return index just after 'ముగింపు'
    return i + 1


# ---------------------------
# Block executor (while)
# ---------------------------
def run_lipi_while_block(lines, start_index, env):
    """
    Processes a WHILE (వరకు) block starting at start_index.
    Returns next index to continue execution.

    NOTE (v0.3): while-body supports only simple single-line
    statements (చెప్పు, అసైన్‌మెంట్). Nested if/while will come later.
    """

    line = lines[start_index].strip()

    if not (line.startswith("వరకు ") and line.endswith(":")):
        return start_index

    condition_expr = line[len("వరకు "):-1].strip()

    # Collect body
    body = []
    i = start_index + 1
    while i < len(lines):
        stripped = lines[i].strip()

        # END of block
        if stripped == "ముగింపు":
            break

        body.append(stripped)
        i += 1

    # Execute loop
    while True:
        condition_value = eval_lipi_expr(condition_expr, env)
        if not bool(condition_value):
            break

        for statement in body:
            run_lipi_line(statement, env)

    # Return index just after 'ముగింపు'
    return i + 1


# ---------------------------
# File runner
# ---------------------------
def run_lipi_file(path):
    env = {}

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty / comments
        if not line or line.startswith("#"):
            i += 1
            continue

        # IF block detected
        if line.startswith("యెడల ") and line.endswith(":"):
            try:
                i = run_lipi_if_block(lines, i, env)
            except Exception as e:
                print(f"[లోపం] లైన్ {i + 1}: {e}")
                break
            continue

        # WHILE block detected
        if line.startswith("వరకు ") and line.endswith(":"):
            try:
                i = run_lipi_while_block(lines, i, env)
            except Exception as e:
                print(f"[లోపం] లైన్ {i + 1}: {e}")
                break
            continue

        # Single-line statement
        try:
            run_lipi_line(line, env)
        except Exception as e:
            print(f"[లోపం] లైన్ {i + 1}: {e}")
            break

        i += 1


# ---------------------------
# REPL
# ---------------------------
def repl():
    """
    Simple interactive shell for Lipi.
    """
    print("Lipi v0.3 REPL – తెలుగు లో కోడ్ రాయండి (Ctrl+C తో బయటకు రావచ్చు)")
    env = {}
    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nవీడ్కోలు! (Goodbye!)")
            break

        try:
            # For now, REPL does not support multi-line blocks
            run_lipi_line(line, env)
        except Exception as e:
            print(f"[లోపం] {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_lipi_file(sys.argv[1])
    else:
        repl()
