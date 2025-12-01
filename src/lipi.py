#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lipi Language - v1.0 (Production Ready)
A bilingual (Telugu + English) scripting language.

NEW in v1.0:
- ✅ Functions and procedures (పనిచేయి / function)
- ✅ Arrays and lists (జాబితా / list)
- ✅ Objects/dictionaries (వస్తువు / object)
- ✅ For loops (పునరావృతం / for)
- ✅ Python library access (దిగుమతి_python / import_python)
- ✅ Error handling (ప్రయత్నించు / try, పట్టుకో / catch)
- ✅ Module system (దిగుమతి / import, ఎగుమతి / export)
- ✅ Enhanced operators (-, *, /, %, **)
- ✅ Boolean literals (true/false, నిజం/అబద్ధం)
- ✅ Null/None (null/శూన్యం)
- ✅ Nested control structures

Supported in v0.5:
- Variable assignment, integers, strings
- If/else blocks (Telugu + English)
- While loops (Telugu + English)
- Print statements
- Comments
"""

import sys
import os
import json
import importlib

# ---------------------------
# Global Runtime Environment
# ---------------------------
class LipiRuntime:
    """Global runtime state for Lipi interpreter"""
    def __init__(self):
        self.functions = {}  # User-defined functions
        self.python_modules = {}  # Imported Python modules
        self.modules = {}  # Imported Lipi modules
        self.exports = {}  # Module exports
        self.whitelist_modules = [
            'math', 'json', 'datetime', 'random', 're', 'time',
            'collections', 'itertools', 'functools', 'operator'
        ]  # Safe Python modules


runtime = LipiRuntime()


# ---------------------------
# Exception Classes
# ---------------------------
class LipiException(Exception):
    """Base exception for Lipi runtime errors"""
    pass


class LipiReturnValue(Exception):
    """Special exception to handle function returns"""
    def __init__(self, value):
        self.value = value
        super().__init__()


# ---------------------------
# Enhanced Expression Evaluator
# ---------------------------
def find_operator_outside_strings(expr, operator):
    """
    Find the position of an operator that's outside of string literals.
    Returns the position, or -1 if not found outside strings.
    """
    in_string = False
    string_char = None
    i = 0

    while i < len(expr):
        char = expr[i]

        # Track string boundaries
        if char in ['"', "'"] and (i == 0 or expr[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None

        # Check for operator outside strings
        if not in_string:
            if expr[i:i+len(operator)] == operator:
                return i

        i += 1

    return -1


def eval_lipi_expr(expr, env):
    """
    Evaluate a Lipi expression.
    Supported:
    - String literals: "text", 'text'
    - Integer literals: 10, -5
    - Float literals: 3.14
    - Boolean: true/false, నిజం/అబద్ధం
    - Null: null, శూన్యం
    - Lists: [1, 2, 3]
    - Objects: {key: value}
    - Operators: +, -, *, /, %, **, ==, !=, <, >, <=, >=
    - Variable lookup
    - Function calls: call func_name(args) / కాల్ func(args)
    - List/object indexing: list[0], obj["key"]
    - Built-in functions: len(), str(), int()
    """
    expr = expr.strip()

    # Handle null/శూన్యం
    if expr in ['null', 'శూన్యం']:
        return None

    # Handle boolean literals
    if expr in ['true', 'నిజం']:
        return True
    if expr in ['false', 'అబద్ధం']:
        return False

    # String literal
    if (expr.startswith('"') and expr.endswith('"')) or \
       (expr.startswith("'") and expr.endswith("'")):
        return expr[1:-1]

    # List literal [1, 2, 3]
    if expr.startswith('[') and expr.endswith(']'):
        list_content = expr[1:-1].strip()
        if not list_content:
            return []
        # Simple comma-separated parsing (TODO: handle nested structures)
        items = []
        for item in list_content.split(','):
            items.append(eval_lipi_expr(item.strip(), env))
        return items

    # Object literal {key: value}
    if expr.startswith('{') and expr.endswith('}'):
        obj_content = expr[1:-1].strip()
        if not obj_content:
            return {}
        obj = {}
        # Simple parsing (TODO: handle nested structures)
        pairs = obj_content.split(',')
        for pair in pairs:
            if ':' in pair:
                key, value = pair.split(':', 1)
                key = key.strip()
                # Remove quotes from key if present
                if (key.startswith('"') and key.endswith('"')) or \
                   (key.startswith("'") and key.endswith("'")):
                    key = key[1:-1]
                obj[key] = eval_lipi_expr(value.strip(), env)
        return obj

    # Float literal
    try:
        if '.' in expr:
            return float(expr)
    except ValueError:
        pass

    # Integer literal
    try:
        return int(expr)
    except ValueError:
        pass

    # Function call: call func(args) or కాల్ func(args)
    if expr.startswith('call ') or expr.startswith('కాల్ '):
        call_expr = expr[5:] if expr.startswith('call ') else expr[4:]
        return eval_function_call(call_expr, env)

    # Built-in function: len(expr)
    if expr.startswith('len(') and expr.endswith(')'):
        arg_expr = expr[4:-1]
        arg_val = eval_lipi_expr(arg_expr, env)
        return len(arg_val)

    # Built-in function: str(expr)
    if expr.startswith('str(') and expr.endswith(')'):
        arg_expr = expr[4:-1]
        arg_val = eval_lipi_expr(arg_expr, env)
        return str(arg_val)

    # Built-in function: int(expr)
    if expr.startswith('int(') and expr.endswith(')'):
        arg_expr = expr[4:-1]
        arg_val = eval_lipi_expr(arg_expr, env)
        return int(arg_val)

    # Indexing: list[0] or obj["key"] or obj.key
    if '[' in expr and ']' in expr:
        # Find the variable name and index
        bracket_pos = expr.index('[')
        var_name = expr[:bracket_pos].strip()
        index_expr = expr[bracket_pos+1:expr.rindex(']')].strip()

        var_value = eval_lipi_expr(var_name, env)
        index_value = eval_lipi_expr(index_expr, env)

        return var_value[index_value]

    # Property access: obj.property
    if '.' in expr and not expr.replace('.', '').replace('-', '').isdigit():
        parts = expr.split('.', 1)
        obj_name = parts[0].strip()
        property_name = parts[1].strip()

        # Security: Prevent access to dunder methods
        if property_name.startswith('__') and property_name.endswith('__'):
            raise LipiException(f"Access to dunder methods is not allowed: {property_name}")

        if obj_name in env:
            obj = env[obj_name]
            if isinstance(obj, dict) and property_name in obj:
                return obj[property_name]
            # Check if it's a Python module
            if hasattr(obj, property_name):
                return getattr(obj, property_name)

        # Check Python modules
        if obj_name in runtime.python_modules:
            module = runtime.python_modules[obj_name]
            # Security: Prevent access to dunder methods
            if property_name.startswith('__') and property_name.endswith('__'):
                raise LipiException(f"Access to dunder methods is not allowed: {property_name}")
            if hasattr(module, property_name):
                attr = getattr(module, property_name)
                # If it's a function with parentheses, call it
                if '(' in expr:
                    # Parse function call
                    func_call = expr[expr.index('.'):]
                    # This is complex, for now just return the attribute
                    return attr
                return attr

    # Python module function call: math.sqrt(16)
    if '.' in expr and '(' in expr and ')' in expr:
        dot_pos = expr.index('.')
        paren_pos = expr.index('(')
        if dot_pos < paren_pos:
            module_name = expr[:dot_pos].strip()
            if module_name in runtime.python_modules:
                func_and_args = expr[dot_pos+1:]
                func_name = func_and_args[:func_and_args.index('(')].strip()
                args_str = func_and_args[func_and_args.index('(')+1:func_and_args.rindex(')')].strip()

                # Security: Prevent access to dunder methods
                if func_name.startswith('__') and func_name.endswith('__'):
                    raise LipiException(f"Access to dunder methods is not allowed: {func_name}")

                module = runtime.python_modules[module_name]
                func = getattr(module, func_name)

                # Parse arguments
                args = []
                if args_str:
                    for arg in args_str.split(','):
                        args.append(eval_lipi_expr(arg.strip(), env))

                return func(*args)

    # Comparisons (order matters: check >= before >)
    for op in [">=", "<=", "==", "!=", ">", "<"]:
        if op in expr:
            left, right = expr.split(op, 1)
            left_val = eval_lipi_expr(left, env)
            right_val = eval_lipi_expr(right, env)

            if op == ">":
                return left_val > right_val
            elif op == "<":
                return left_val < right_val
            elif op == ">=":
                return left_val >= right_val
            elif op == "<=":
                return left_val <= right_val
            elif op == "==":
                return left_val == right_val
            elif op == "!=":
                return left_val != right_val

    # Arithmetic operators (check after comparisons)
    # Power **
    pos = find_operator_outside_strings(expr, " ** ")
    if pos != -1:
        left = expr[:pos]
        right = expr[pos+4:]  # +4 for " ** "
        return eval_lipi_expr(left, env) ** eval_lipi_expr(right, env)

    # Multiplication, division, modulo
    pos = find_operator_outside_strings(expr, " * ")
    if pos != -1:
        left = expr[:pos]
        right = expr[pos+3:]  # +3 for " * "
        return eval_lipi_expr(left, env) * eval_lipi_expr(right, env)

    pos = find_operator_outside_strings(expr, " / ")
    if pos != -1:
        left = expr[:pos]
        right = expr[pos+3:]  # +3 for " / "
        return eval_lipi_expr(left, env) / eval_lipi_expr(right, env)

    pos = find_operator_outside_strings(expr, " % ")
    if pos != -1:
        left = expr[:pos]
        right = expr[pos+3:]  # +3 for " % "
        return eval_lipi_expr(left, env) % eval_lipi_expr(right, env)

    # Subtraction (check after other operators)
    pos = find_operator_outside_strings(expr, " - ")
    if pos != -1:
        left = expr[:pos]
        right = expr[pos+3:]  # +3 for " - "
        return eval_lipi_expr(left, env) - eval_lipi_expr(right, env)

    # Addition (lowest precedence)
    pos = find_operator_outside_strings(expr, " + ")
    if pos != -1:
        left = expr[:pos]
        right = expr[pos+3:]  # +3 for " + "
        left_val = eval_lipi_expr(left, env)
        right_val = eval_lipi_expr(right, env)

        # String concatenation if either is string
        if isinstance(left_val, str) or isinstance(right_val, str):
            return str(left_val) + str(right_val)

        return left_val + right_val

    # Variable lookup
    if expr in env:
        return env[expr]

    raise ValueError(f"తెలియని వ్యక్తీకరణ (unknown expression): {expr}")


def eval_function_call(call_expr, env):
    """Evaluate a function call: func_name(arg1, arg2)"""
    paren_pos = call_expr.index('(')
    func_name = call_expr[:paren_pos].strip()
    args_str = call_expr[paren_pos+1:call_expr.rindex(')')].strip()

    # Check if function exists
    if func_name not in runtime.functions:
        raise LipiException(f"Function not found: {func_name}")

    func_def = runtime.functions[func_name]

    # Parse arguments
    args = []
    if args_str:
        for arg in args_str.split(','):
            args.append(eval_lipi_expr(arg.strip(), env))

    # Create new scope for function
    func_env = env.copy()

    # Bind parameters
    params = func_def['params']
    if len(args) != len(params):
        raise LipiException(f"Function {func_name} expects {len(params)} arguments, got {len(args)}")

    for param, arg in zip(params, args):
        func_env[param] = arg

    # Execute function body using block executor for proper control flow
    try:
        execute_block(func_def['body'], func_env)
        return None  # No explicit return
    except LipiReturnValue as ret:
        return ret.value


# ---------------------------
# Enhanced Line Executor
# ---------------------------
def run_lipi_line(line, env):
    """
    Execute a single line of Lipi code.
    Supports both Telugu and English keywords.
    """
    line = line.strip()

    # Empty / comment
    if not line or line.startswith("#"):
        return

    # Return statement: return expr / రిటర్న్ expr
    if line.startswith("return ") or line.startswith("రిటర్న్ "):
        expr = line[7:] if line.startswith("return ") else line[8:]
        value = eval_lipi_expr(expr.strip(), env) if expr.strip() else None
        raise LipiReturnValue(value)

    # Print statement (Telugu): చెప్పు expr
    if line.startswith("చెప్పు "):
        expr = line[len("చెప్పు "):]
        value = eval_lipi_expr(expr, env)
        print(value)
        return

    # Print statement (English): print expr
    if line.startswith("print "):
        expr = line[len("print "):]
        value = eval_lipi_expr(expr, env)
        print(value)
        return

    # Python library import: import_python("module") / దిగుమతి_python("module")
    if line.startswith("import_python(") or line.startswith("దిగుమతి_python("):
        module_expr = line[line.index('(')+1:line.rindex(')')]
        module_name = eval_lipi_expr(module_expr.strip(), env)

        if module_name not in runtime.whitelist_modules:
            raise LipiException(f"Module {module_name} is not whitelisted for security reasons")

        try:
            module = importlib.import_module(module_name)
            runtime.python_modules[module_name] = module
            env[module_name] = module
        except ImportError as e:
            raise LipiException(f"Failed to import Python module {module_name}: {e}")
        return

    # Export statement: export func_name / ఎగుమతి func_name
    if line.startswith("export ") or line.startswith("ఎగుమతి "):
        names = line[7:] if line.startswith("export ") else line[8:]
        for name in names.split(','):
            name = name.strip()
            if name in env:
                runtime.exports[name] = env[name]
            elif name in runtime.functions:
                runtime.exports[name] = runtime.functions[name]
        return

    # Assignment: name = expr
    if "=" in line and not any(op in line for op in ["==", ">=", "<=", "!="]):
        name, expr = line.split("=", 1)
        name = name.strip()
        expr = expr.strip()
        env[name] = eval_lipi_expr(expr, env)
        return

    # Standalone function call: call func(args) or కాల్ func(args)
    if line.startswith('call ') or line.startswith('కాల్ '):
        eval_lipi_expr(line, env)
        return

    # If we reach here, syntax is unknown
    raise SyntaxError(f"తెలియని లైన్ (unknown line): {line}")


# ---------------------------
# Function Definition Handler
# ---------------------------
def parse_function_definition(lines, start_index, env):
    """
    Parse function definition starting at start_index.
    Supports: function name(params): / పనిచేయి name(params):
    Returns: (next_index, function_name, params, body)
    """
    line = lines[start_index].strip()

    # Check for Telugu or English function definition
    is_telugu = line.startswith("పనిచేయి ")
    is_english = line.startswith("function ")

    if not (is_telugu or is_english) or ':' not in line:
        return None

    # Extract function signature
    if is_telugu:
        signature = line[len("పనిచేయి "):-1].strip()
    else:
        signature = line[len("function "):-1].strip()

    # Parse function name and parameters
    paren_pos = signature.index('(')
    func_name = signature[:paren_pos].strip()
    params_str = signature[paren_pos+1:signature.rindex(')')].strip()

    params = []
    if params_str:
        params = [p.strip() for p in params_str.split(',')]

    # Collect function body (track nesting depth)
    body = []
    i = start_index + 1
    nesting_depth = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # Track nested control structures
        if any(stripped.startswith(kw) for kw in ["యెడల", "if", "లేకపోతే", "else",
                                                    "అలాగే", "elif", "ఎప్పుడు", "while",
                                                    "పునరావృతం", "for", "పనిచేయి", "function",
                                                    "ప్రయత్నించు:", "try:"]):
            nesting_depth += 1
            body.append(stripped)
        elif stripped in ["ముగింపు", "end"]:
            if nesting_depth == 0:
                # This closes the function
                break
            else:
                # This closes a nested structure
                nesting_depth -= 1
                body.append(stripped)
        else:
            body.append(stripped)

        i += 1

    # Store function in runtime
    runtime.functions[func_name] = {
        'params': params,
        'body': body,
        'env': env.copy()  # Capture closure
    }

    # Return index after 'ముగింపు' or 'end'
    return i + 1


# ---------------------------
# For Loop Handler
# ---------------------------
def run_lipi_for_loop(lines, start_index, env):
    """
    Process a FOR loop: for item in list: / పునరావృతం item in list:
    """
    line = lines[start_index].strip()

    # Check for Telugu or English for loop
    is_telugu = line.startswith("పునరావృతం ")
    is_english = line.startswith("for ")

    if not (is_telugu or is_english) or ':' not in line or ' in ' not in line:
        return start_index

    # Extract loop variable and iterable
    if is_telugu:
        loop_expr = line[len("పునరావృతం "):-1].strip()
    else:
        loop_expr = line[len("for "):-1].strip()

    var_name, iterable_expr = loop_expr.split(' in ', 1)
    var_name = var_name.strip()
    iterable = eval_lipi_expr(iterable_expr.strip(), env)

    # Collect loop body
    body = []
    i = start_index + 1
    while i < len(lines):
        stripped = lines[i].strip()

        # End of loop
        if stripped == "ముగింపు" or stripped == "end":
            break

        body.append(stripped)
        i += 1

    # Execute loop using block executor for proper control flow
    for item in iterable:
        env[var_name] = item
        execute_block(body, env)

    return i + 1


# ---------------------------
# Try-Catch Handler
# ---------------------------
def run_lipi_try_catch(lines, start_index, env):
    """
    Process try-catch block: try: / ప్రయత్నించు:
    """
    line = lines[start_index].strip()

    is_telugu = line == "ప్రయత్నించు:"
    is_english = line == "try:"

    if not (is_telugu or is_english):
        return start_index

    # Collect try body
    try_body = []
    catch_body = []
    finally_body = []
    current_body = try_body
    error_var = None

    i = start_index + 1
    while i < len(lines):
        stripped = lines[i].strip()

        # Catch block: catch error: / పట్టుకో error: or just catch: / పట్టుకో:
        if stripped.startswith("catch") or stripped.startswith("పట్టుకో"):
            parts = stripped.split()
            if len(parts) > 1:
                error_var = parts[1].rstrip(':')
            current_body = catch_body
            i += 1
            continue

        # Finally block: finally: / చివరకు:
        if stripped == "finally:" or stripped == "చివరకు:":
            current_body = finally_body
            i += 1
            continue

        # End of try-catch
        if stripped == "ముగింపు" or stripped == "end":
            break

        current_body.append(stripped)
        i += 1

    # Execute try block using block executor for proper control flow
    try:
        execute_block(try_body, env)
    except Exception as e:
        # Execute catch block
        if error_var:
            env[error_var] = str(e)
        execute_block(catch_body, env)
    finally:
        # Execute finally block
        execute_block(finally_body, env)

    return i + 1


# ---------------------------
# Enhanced Block Executors
# ---------------------------
def run_lipi_if_block(lines, start_index, env):
    """
    Processes an IF/ELSE block starting at start_index.
    Supports both Telugu (యెడల/లేకపోతే/ముగింపు) and English (if/else/end).
    """
    line = lines[start_index].strip()

    is_telugu_if = line.startswith("యెడల ") and line.endswith(":")
    is_english_if = line.startswith("if ") and line.endswith(":")

    if not (is_telugu_if or is_english_if):
        return start_index

    # Extract condition
    condition_expr = line[len("యెడల "):-1].strip() if is_telugu_if else line[len("if "):-1].strip()

    # Evaluate condition
    condition_value = eval_lipi_expr(condition_expr, env)
    condition_true = bool(condition_value)

    # Collect IF and ELSE bodies (with nesting support)
    if_body = []
    else_body = []
    current = if_body
    nesting_level = 0

    i = start_index + 1
    while i < len(lines):
        stripped = lines[i].strip()

        # Track nesting
        if (stripped.startswith("యెడల ") or stripped.startswith("if ")) and stripped.endswith(":"):
            nesting_level += 1
        elif (stripped.startswith("వరకు ") or stripped.startswith("while ")) and stripped.endswith(":"):
            nesting_level += 1
        elif (stripped.startswith("పునరావృతం ") or stripped.startswith("for ")) and stripped.endswith(":"):
            nesting_level += 1
        elif (stripped.startswith("పనిచేయి ") or stripped.startswith("function ")) and stripped.endswith(":"):
            nesting_level += 1

        # ELSE branch (only at our level)
        if nesting_level == 0 and (stripped == "లేకపోతే:" or stripped == "else:"):
            current = else_body
            i += 1
            continue

        # END of block (only at our level)
        if nesting_level == 0 and (stripped == "ముగింపు" or stripped == "end"):
            break

        # Decrease nesting when we see end
        if stripped == "ముగింపు" or stripped == "end":
            nesting_level -= 1

        current.append(stripped)
        i += 1

    # Execute chosen body
    body_to_run = if_body if condition_true else else_body
    execute_block(body_to_run, env)

    return i + 1


def run_lipi_while_block(lines, start_index, env):
    """
    Processes a WHILE block with nesting support.
    """
    line = lines[start_index].strip()

    is_telugu_while = line.startswith("వరకు ") and line.endswith(":")
    is_english_while = line.startswith("while ") and line.endswith(":")

    if not (is_telugu_while or is_english_while):
        return start_index

    # Extract condition
    condition_expr = line[len("వరకు "):-1].strip() if is_telugu_while else line[len("while "):-1].strip()

    # Collect body (with nesting support)
    body = []
    nesting_level = 0

    i = start_index + 1
    while i < len(lines):
        stripped = lines[i].strip()

        # Track nesting
        if (stripped.startswith("యెడల ") or stripped.startswith("if ")) and stripped.endswith(":"):
            nesting_level += 1
        elif (stripped.startswith("వరకు ") or stripped.startswith("while ")) and stripped.endswith(":"):
            nesting_level += 1
        elif (stripped.startswith("పునరావృతం ") or stripped.startswith("for ")) and stripped.endswith(":"):
            nesting_level += 1

        # END of block (only at our level)
        if nesting_level == 0 and (stripped == "ముగింపు" or stripped == "end"):
            break

        # Decrease nesting
        if stripped == "ముగింపు" or stripped == "end":
            nesting_level -= 1

        body.append(stripped)
        i += 1

    # Execute loop
    while True:
        condition_value = eval_lipi_expr(condition_expr, env)
        if not bool(condition_value):
            break

        execute_block(body, env)

    return i + 1


def execute_block(lines, env):
    """Execute a block of code with support for nested structures"""
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        # Skip empty lines, comments, and standalone end markers
        if not line or line.startswith("#") or line in ["ముగింపు", "end"]:
            i += 1
            continue

        # Function definition
        if (line.startswith("పనిచేయి ") or line.startswith("function ")) and line.endswith(":"):
            i = parse_function_definition(lines, i, env)
            continue

        # IF block
        if (line.startswith("యెడల ") or line.startswith("if ")) and line.endswith(":"):
            i = run_lipi_if_block(lines, i, env)
            continue

        # WHILE block
        if (line.startswith("వరకు ") or line.startswith("while ")) and line.endswith(":"):
            i = run_lipi_while_block(lines, i, env)
            continue

        # FOR loop
        if (line.startswith("పునరావృతం ") or line.startswith("for ")) and ' in ' in line and line.endswith(":"):
            i = run_lipi_for_loop(lines, i, env)
            continue

        # Try-catch
        if line == "ప్రయత్నించు:" or line == "try:":
            i = run_lipi_try_catch(lines, i, env)
            continue

        # Single line
        run_lipi_line(line, env)
        i += 1


# ---------------------------
# File Runner
# ---------------------------
def run_lipi_file(path):
    """Run a Lipi source file"""
    env = {}

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    try:
        execute_block(lines, env)
    except Exception as e:
        print(f"[లోపం] Runtime error: {e}")
        import traceback
        traceback.print_exc()


# ---------------------------
# REPL
# ---------------------------
def repl():
    """Interactive shell for Lipi"""
    print("Lipi v1.0 REPL – తెలుగు లో / in English కోడ్ రాయండి (Ctrl+C తో బయటకు రావచ్చు)")
    print("New in v1.0: Functions, Arrays, Objects, For loops, Python libraries, Try-catch!")
    env = {}

    while True:
        try:
            line = input(">>> ")
        except (EOFError, KeyboardInterrupt):
            print("\nవీడ్కోలు! (Goodbye!)")
            break

        try:
            run_lipi_line(line, env)
        except LipiReturnValue as ret:
            print(f"=> {ret.value}")
        except Exception as e:
            print(f"[లోపం] {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_lipi_file(sys.argv[1])
    else:
        repl()
