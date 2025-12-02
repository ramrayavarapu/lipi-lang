#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lipi Language - v3.0 (Enterprise Scale)
A bilingual (Telugu + English) scripting language.

NEW in v3.0:
- ✅ Full module import system (దిగుమతి / import from "module")
- ✅ OOP Classes with inheritance (క్లాస్ / class, inheritance support)
- ✅ MySQL database support (mysql_కనెక్ట్ / mysql_connect)
- ✅ PostgreSQL database support (postgres_కనెక్ట్ / postgres_connect)
- 🔄 Comprehensive testing & optimization - IN PROGRESS (Day 4-5)

Implemented in v2.0:
- ✅ File I/O (ఫైల్_చదువు / file_read, ఫైల్_వ్రాయి / file_write)
- ✅ HTTP/API support (http_పొందు / http_get, http_పంపు / http_post)
- ✅ Database connectivity (డేటాబేస్_కనెక్ట్ / db_connect, SQLite)

Implemented in v1.0:
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
import importlib
import sqlite3
import urllib.request
import urllib.parse
import json

# v3.0: Optional MySQL support
try:
    import mysql.connector
    MYSQL_AVAILABLE = True
except ImportError:
    MYSQL_AVAILABLE = False

# v3.0: Optional PostgreSQL support
try:
    import psycopg2
    import psycopg2.extras
    POSTGRES_AVAILABLE = True
except ImportError:
    POSTGRES_AVAILABLE = False

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
        self.db_connections = {}  # Database connections
        self.loaded_modules = {}  # v3.0: Track loaded module exports
        self.module_stack = []  # v3.0: Detect circular imports
        self.current_module_path = None  # v3.0: Track current module for relative imports
        self.classes = {}  # v3.0: User-defined classes
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
# v3.0: Module Import System
# ---------------------------

def resolve_module_path(module_name, current_file_path=None):
    """
    Resolve module path relative to current file or absolute.

    Args:
        module_name: Module name like "utils" or "models/user"
        current_file_path: Path of file doing the import

    Returns:
        Absolute path to module file
    """
    # Security: Prevent path traversal
    if '..' in module_name or module_name.startswith('/'):
        raise LipiException(f"Invalid module path: {module_name}. Path traversal not allowed.")

    # Add .lipi.py extension if not present
    if not module_name.endswith('.lipi.py'):
        module_file = module_name + '.lipi.py'
    else:
        module_file = module_name

    # If current file path provided, resolve relative to it
    if current_file_path:
        current_dir = os.path.dirname(os.path.abspath(current_file_path))
        module_path = os.path.join(current_dir, module_file)
    else:
        # Resolve relative to current working directory
        module_path = os.path.abspath(module_file)

    return module_path


def load_lipi_module(module_path, runtime, parent_env):
    """
    Load a Lipi module file and return its exports.

    Args:
        module_path: Absolute path to .lipi.py file
        runtime: LipiRuntime instance
        parent_env: Parent environment (for variable access)

    Returns:
        Dictionary of exported functions/variables
    """
    # Check if already loaded (module caching)
    if module_path in runtime.loaded_modules:
        return runtime.loaded_modules[module_path]

    # Check for circular imports
    if module_path in runtime.module_stack:
        cycle = ' -> '.join(runtime.module_stack + [module_path])
        raise LipiException(f"Circular import detected: {cycle}")

    # Check if file exists
    if not os.path.exists(module_path):
        raise LipiException(f"Module not found: {module_path}")

    # Push to module stack
    runtime.module_stack.append(module_path)
    prev_module_path = runtime.current_module_path
    runtime.current_module_path = module_path

    try:
        # Read module file
        with open(module_path, 'r', encoding='utf-8') as f:
            module_code = f.read()

        # Create new environment for module
        module_env = parent_env.copy()  # Inherit parent scope
        module_exports = {}

        # Split into lines
        lines = module_code.split('\n')

        # Track what to export (collect export statements first)
        temp_exports_list = []
        filtered_lines = []

        for line in lines:
            stripped = line.strip()
            # Collect export statements but don't execute them
            if stripped.startswith('ఎగుమతి ') or stripped.startswith('export '):
                export_keyword = 'ఎగుమతి ' if stripped.startswith('ఎగుమతి ') else 'export '
                exports_str = stripped[len(export_keyword):].strip()
                export_names = [name.strip() for name in exports_str.split(',')]
                temp_exports_list.extend(export_names)
            else:
                # Keep non-export lines for execution
                filtered_lines.append(line)

        # Execute the module code (handles multi-line functions properly)
        try:
            execute_block(filtered_lines, module_env)
        except LipiReturnValue:
            # Returns shouldn't escape module scope
            pass

        # Collect exported items
        for export_name in temp_exports_list:
            if export_name in module_env:
                module_exports[export_name] = module_env[export_name]
            elif export_name in runtime.functions:
                module_exports[export_name] = runtime.functions[export_name]
            else:
                raise LipiException(f"Cannot export '{export_name}': not defined in module")

        # Cache the module exports
        runtime.loaded_modules[module_path] = module_exports

        return module_exports

    finally:
        # Pop from module stack
        runtime.module_stack.pop()
        runtime.current_module_path = prev_module_path


def parse_import_statement(line, runtime, env):
    """
    Parse import statement and load module.

    Syntax:
        దిగుమతి function_name from "module_path"
        import function_name from "module_path"
        దిగుమతి function1, function2 from "module"

    Args:
        line: Import statement line
        runtime: LipiRuntime instance
        env: Current environment
    """
    # Determine which keyword is used
    if line.startswith('దిగుమతి '):
        keyword = 'దిగుమతి '
    elif line.startswith('import '):
        keyword = 'import '
    else:
        raise LipiException(f"Invalid import statement: {line}")

    # Remove keyword
    import_spec = line[len(keyword):].strip()

    # Check for "from" keyword
    if ' from ' in import_spec:
        parts = import_spec.split(' from ')
        if len(parts) != 2:
            raise LipiException(f"Invalid import syntax: {line}")

        import_names_str, module_name_quoted = parts

        # Parse imported names (can be comma-separated)
        import_names = [name.strip() for name in import_names_str.split(',')]

        # Remove quotes from module name
        module_name = module_name_quoted.strip()
        if (module_name.startswith('"') and module_name.endswith('"')) or \
           (module_name.startswith("'") and module_name.endswith("'")):
            module_name = module_name[1:-1]
        else:
            raise LipiException(f"Module name must be quoted: {module_name_quoted}")

        # Resolve module path
        module_path = resolve_module_path(module_name, runtime.current_module_path)

        # Load module
        module_exports = load_lipi_module(module_path, runtime, env)

        # Import requested names into current environment
        for import_name in import_names:
            if import_name not in module_exports:
                raise LipiException(f"Module '{module_name}' does not export '{import_name}'")

            # Add to current environment
            if callable(module_exports[import_name]):
                # It's a function - add to runtime.functions
                runtime.functions[import_name] = module_exports[import_name]
            else:
                # It's a variable - add to environment
                env[import_name] = module_exports[import_name]

    else:
        raise LipiException(f"Import statement must use 'from' keyword: {line}")


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


def split_arguments(args_str):
    """
    Split function arguments by comma, respecting string boundaries and parentheses.
    Example: 'a, "b, c", d' -> ['a', '"b, c"', 'd']
    """
    args = []
    current = []
    in_string = False
    string_char = None
    paren_depth = 0
    bracket_depth = 0

    for i, char in enumerate(args_str):
        # Track string boundaries
        if char in ['"', "'"] and (i == 0 or args_str[i-1] != '\\'):
            if not in_string:
                in_string = True
                string_char = char
            elif char == string_char:
                in_string = False
                string_char = None

        # Track parentheses and brackets
        if not in_string:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1

            # Split on comma only if not in string and all brackets/parens are balanced
            if char == ',' and paren_depth == 0 and bracket_depth == 0:
                args.append(''.join(current).strip())
                current = []
                continue

        current.append(char)

    # Add last argument
    if current:
        args.append(''.join(current).strip())

    return args


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

    # String literal (only if no operators outside quotes)
    if (expr.startswith('"') and expr.endswith('"')) or \
       (expr.startswith("'") and expr.endswith("'")):
        # Check if there are operators outside string boundaries
        # If there's a + operator outside strings, it's not a simple string literal
        if find_operator_outside_strings(expr, " + ") == -1 and \
           find_operator_outside_strings(expr, " - ") == -1:
            return expr[1:-1]
        # Otherwise, fall through to operator handling below

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

    # File I/O: file_read(path) / ఫైల్_చదువు(path)
    if expr.startswith('file_read(') or expr.startswith('ఫైల్_చదువు('):
        start = len('file_read(') if expr.startswith('file_read(') else len('ఫైల్_చదువు(')
        arg_expr = expr[start:-1]
        file_path = eval_lipi_expr(arg_expr, env)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            raise LipiException(f"File read error: {e}")

    # File I/O: file_write(path, content) / ఫైల్_వ్రాయి(path, content)
    if expr.startswith('file_write(') or expr.startswith('ఫైల్_వ్రాయి('):
        start = len('file_write(') if expr.startswith('file_write(') else len('ఫైల్_వ్రాయి(')
        args_expr = expr[start:-1]
        args = split_arguments(args_expr)
        if len(args) != 2:
            raise LipiException("file_write requires 2 arguments: path and content")
        file_path = eval_lipi_expr(args[0], env)
        content = eval_lipi_expr(args[1], env)
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(str(content))
            return True
        except Exception as e:
            raise LipiException(f"File write error: {e}")

    # File I/O: file_append(path, content) / ఫైల్_జోడించు(path, content)
    if expr.startswith('file_append(') or expr.startswith('ఫైల్_జోడించు('):
        start = len('file_append(') if expr.startswith('file_append(') else len('ఫైల్_జోడించు(')
        args_expr = expr[start:-1]
        args = split_arguments(args_expr)
        if len(args) != 2:
            raise LipiException("file_append requires 2 arguments: path and content")
        file_path = eval_lipi_expr(args[0], env)
        content = eval_lipi_expr(args[1], env)
        try:
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(str(content))
            return True
        except Exception as e:
            raise LipiException(f"File append error: {e}")

    # HTTP: http_get(url) / http_పొందు(url)
    if expr.startswith('http_get(') or expr.startswith('http_పొందు('):
        start = len('http_get(') if expr.startswith('http_get(') else len('http_పొందు(')
        arg_expr = expr[start:-1]
        url = eval_lipi_expr(arg_expr, env)
        try:
            with urllib.request.urlopen(url) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            raise LipiException(f"HTTP GET error: {e}")

    # HTTP: http_post(url, data) / http_పంపు(url, data)
    if expr.startswith('http_post(') or expr.startswith('http_పంపు('):
        start = len('http_post(') if expr.startswith('http_post(') else len('http_పంపు(')
        args_expr = expr[start:-1]
        args = split_arguments(args_expr)
        if len(args) != 2:
            raise LipiException("http_post requires 2 arguments: url and data")
        url = eval_lipi_expr(args[0], env)
        data = eval_lipi_expr(args[1], env)
        try:
            # Convert dict to JSON if needed
            if isinstance(data, dict):
                data = json.dumps(data)
            data_bytes = data.encode('utf-8')
            req = urllib.request.Request(url, data=data_bytes, headers={'Content-Type': 'application/json'})
            with urllib.request.urlopen(req) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            raise LipiException(f"HTTP POST error: {e}")

    # Database: db_connect(path) / డేటాబేస్_కనెక్ట్(path)
    if expr.startswith('db_connect(') or expr.startswith('డేటాబేస్_కనెక్ట్('):
        start = len('db_connect(') if expr.startswith('db_connect(') else len('డేటాబేస్_కనెక్ట్(')
        arg_expr = expr[start:-1]
        db_path = eval_lipi_expr(arg_expr, env)
        try:
            conn = sqlite3.connect(db_path)
            conn_id = f"db_{id(conn)}"
            runtime.db_connections[conn_id] = conn
            return conn_id
        except Exception as e:
            raise LipiException(f"Database connection error: {e}")

    # Database: db_query(conn_id, sql) / డేటాబేస్_ప్రశ్న(conn_id, sql)
    if expr.startswith('db_query(') or expr.startswith('డేటాబేస్_ప్రశ్న('):
        start = len('db_query(') if expr.startswith('db_query(') else len('డేటాబేస్_ప్రశ్న(')
        args_expr = expr[start:-1]
        args = split_arguments(args_expr)
        if len(args) != 2:
            raise LipiException("db_query requires 2 arguments: connection_id and sql")
        conn_id = eval_lipi_expr(args[0], env)
        sql = eval_lipi_expr(args[1], env)
        try:
            if conn_id not in runtime.db_connections:
                raise LipiException(f"Invalid database connection: {conn_id}")
            conn = runtime.db_connections[conn_id]
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            # Return results for SELECT, row count for other operations
            if sql.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                # Convert to list of dicts
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in results]
            return cursor.rowcount
        except Exception as e:
            raise LipiException(f"Database query error: {e}")

    # Database: db_close(conn_id) / డేటాబేస్_మూసివేయి(conn_id)
    if expr.startswith('db_close(') or expr.startswith('డేటాబేస్_మూసివేయి('):
        start = len('db_close(') if expr.startswith('db_close(') else len('డేటాబేస్_మూసివేయి(')
        arg_expr = expr[start:-1]
        conn_id = eval_lipi_expr(arg_expr, env)
        try:
            if conn_id in runtime.db_connections:
                runtime.db_connections[conn_id].close()
                del runtime.db_connections[conn_id]
                return True
            return False
        except Exception as e:
            raise LipiException(f"Database close error: {e}")

    # MySQL: mysql_connect(host, user, password, database) / mysql_కనెక్ట్(...) (v3.0)
    if expr.startswith('mysql_connect(') or expr.startswith('mysql_కనెక్ట్('):
        if not MYSQL_AVAILABLE:
            raise LipiException("MySQL connector not available. Install: pip install mysql-connector-python")

        start = len('mysql_connect(') if expr.startswith('mysql_connect(') else len('mysql_కనెక్ట్(')
        args_expr = expr[start:-1]
        args = [arg.strip() for arg in split_arguments(args_expr)]

        if len(args) != 4:
            raise LipiException("mysql_connect requires 4 arguments: (host, user, password, database)")

        host = eval_lipi_expr(args[0], env)
        user = eval_lipi_expr(args[1], env)
        password = eval_lipi_expr(args[2], env)
        database = eval_lipi_expr(args[3], env)

        try:
            conn = mysql.connector.connect(
                host=host,
                user=user,
                password=password,
                database=database
            )
            conn_id = f"mysql_{id(conn)}"
            runtime.db_connections[conn_id] = conn
            return conn_id
        except Exception as e:
            raise LipiException(f"MySQL connection error: {e}")

    # MySQL: mysql_query(conn_id, sql, [params]) / mysql_ప్రశ్న(...) (v3.0)
    if expr.startswith('mysql_query(') or expr.startswith('mysql_ప్రశ్న('):
        if not MYSQL_AVAILABLE:
            raise LipiException("MySQL connector not available. Install: pip install mysql-connector-python")

        start = len('mysql_query(') if expr.startswith('mysql_query(') else len('mysql_ప్రశ్న(')
        args_expr = expr[start:-1]
        args = [arg.strip() for arg in split_arguments(args_expr)]

        if len(args) < 2:
            raise LipiException("mysql_query requires at least 2 arguments: (conn_id, sql, [params])")

        conn_id = eval_lipi_expr(args[0], env)
        sql = eval_lipi_expr(args[1], env)
        params = None
        if len(args) >= 3:
            params = eval_lipi_expr(args[2], env)
            if not isinstance(params, (list, tuple)):
                params = [params]

        try:
            if conn_id not in runtime.db_connections:
                raise LipiException(f"Invalid MySQL connection: {conn_id}")

            conn = runtime.db_connections[conn_id]
            cursor = conn.cursor(dictionary=True)  # Return results as dictionaries

            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            conn.commit()

            # Fetch results if it's a SELECT query
            if sql.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                cursor.close()
                return results
            else:
                # For INSERT/UPDATE/DELETE, return affected rows
                affected = cursor.rowcount
                cursor.close()
                return affected
        except Exception as e:
            raise LipiException(f"MySQL query error: {e}")

    # MySQL: mysql_close(conn_id) / mysql_మూసివేయి(conn_id) (v3.0)
    if expr.startswith('mysql_close(') or expr.startswith('mysql_మూసివేయి('):
        start = len('mysql_close(') if expr.startswith('mysql_close(') else len('mysql_మూసివేయి(')
        arg_expr = expr[start:-1]
        conn_id = eval_lipi_expr(arg_expr, env)
        try:
            if conn_id in runtime.db_connections and conn_id.startswith('mysql_'):
                runtime.db_connections[conn_id].close()
                del runtime.db_connections[conn_id]
                return True
            return False
        except Exception as e:
            raise LipiException(f"MySQL close error: {e}")

    # PostgreSQL: postgres_connect(host, user, password, database, [port]) / postgres_కనెక్ట్(...) (v3.0)
    if expr.startswith('postgres_connect(') or expr.startswith('postgres_కనెక్ట్('):
        if not POSTGRES_AVAILABLE:
            raise LipiException("PostgreSQL connector not available. Install: pip install psycopg2-binary")

        start = len('postgres_connect(') if expr.startswith('postgres_connect(') else len('postgres_కనెక్ట్(')
        args_expr = expr[start:-1]
        args = [arg.strip() for arg in split_arguments(args_expr)]

        if len(args) < 4:
            raise LipiException("postgres_connect requires at least 4 arguments: (host, user, password, database, [port])")

        host = eval_lipi_expr(args[0], env)
        user = eval_lipi_expr(args[1], env)
        password = eval_lipi_expr(args[2], env)
        database = eval_lipi_expr(args[3], env)
        port = "5432"  # Default PostgreSQL port
        if len(args) >= 5:
            port = eval_lipi_expr(args[4], env)

        try:
            conn = psycopg2.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=port
            )
            conn_id = f"pg_{id(conn)}"
            runtime.db_connections[conn_id] = conn
            return conn_id
        except Exception as e:
            raise LipiException(f"PostgreSQL connection error: {e}")

    # PostgreSQL: postgres_query(conn_id, sql, [params]) / postgres_ప్రశ్న(...) (v3.0)
    if expr.startswith('postgres_query(') or expr.startswith('postgres_ప్రశ్న('):
        if not POSTGRES_AVAILABLE:
            raise LipiException("PostgreSQL connector not available. Install: pip install psycopg2-binary")

        start = len('postgres_query(') if expr.startswith('postgres_query(') else len('postgres_ప్రశ్న(')
        args_expr = expr[start:-1]
        args = [arg.strip() for arg in split_arguments(args_expr)]

        if len(args) < 2:
            raise LipiException("postgres_query requires at least 2 arguments: (conn_id, sql, [params])")

        conn_id = eval_lipi_expr(args[0], env)
        sql = eval_lipi_expr(args[1], env)
        params = None
        if len(args) >= 3:
            params = eval_lipi_expr(args[2], env)
            if not isinstance(params, (list, tuple)):
                params = [params]

        try:
            if conn_id not in runtime.db_connections:
                raise LipiException(f"Invalid PostgreSQL connection: {conn_id}")

            conn = runtime.db_connections[conn_id]
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)  # Return results as dictionaries

            if params:
                cursor.execute(sql, params)
            else:
                cursor.execute(sql)

            conn.commit()

            # Fetch results if it's a SELECT query
            if sql.strip().upper().startswith('SELECT'):
                results = cursor.fetchall()
                # Convert RealDictRow to regular dict
                results = [dict(row) for row in results]
                cursor.close()
                return results
            else:
                # For INSERT/UPDATE/DELETE, return affected rows
                affected = cursor.rowcount
                cursor.close()
                return affected
        except Exception as e:
            raise LipiException(f"PostgreSQL query error: {e}")

    # PostgreSQL: postgres_close(conn_id) / postgres_మూసివేయి(conn_id) (v3.0)
    if expr.startswith('postgres_close(') or expr.startswith('postgres_మూసివేయి('):
        start = len('postgres_close(') if expr.startswith('postgres_close(') else len('postgres_మూసివేయి(')
        arg_expr = expr[start:-1]
        conn_id = eval_lipi_expr(arg_expr, env)
        try:
            if conn_id in runtime.db_connections and conn_id.startswith('pg_'):
                runtime.db_connections[conn_id].close()
                del runtime.db_connections[conn_id]
                return True
            return False
        except Exception as e:
            raise LipiException(f"PostgreSQL close error: {e}")

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

    # Class instantiation: ClassName(args) (v3.0)
    # Check for dots outside strings to distinguish from method calls
    if '(' in expr and ')' in expr and find_operator_outside_strings(expr, ".") == -1:
        paren_pos = expr.index('(')
        potential_class_name = expr[:paren_pos].strip()
        if potential_class_name in runtime.classes:
            # This is class instantiation
            args_str = expr[paren_pos+1:expr.rindex(')')].strip()
            args = []
            if args_str:
                for arg in split_arguments(args_str):
                    args.append(eval_lipi_expr(arg.strip(), env))
            return instantiate_class(potential_class_name, args, env)

    # Method call on instance: instance.method(args) (v3.0)
    if '.' in expr and '(' in expr and ')' in expr:
        dot_pos = expr.index('.')
        paren_pos = expr.index('(')
        if dot_pos < paren_pos:
            obj_name = expr[:dot_pos].strip()
            # Check if this is a class instance (not a Python module)
            if obj_name in env and isinstance(env[obj_name], LipiClassInstance):
                instance = env[obj_name]
                method_and_args = expr[dot_pos+1:]
                method_name = method_and_args[:method_and_args.index('(')].strip()
                args_str = method_and_args[method_and_args.index('(')+1:method_and_args.rindex(')')].strip()

                # Parse arguments
                args = []
                if args_str:
                    for arg in split_arguments(args_str):
                        args.append(eval_lipi_expr(arg.strip(), env))

                return call_method(instance, method_name, args, env)

    # Instance attribute access: instance.attribute (v3.0)
    if '.' in expr and '(' not in expr:
        dot_pos = expr.index('.')
        obj_name = expr[:dot_pos].strip()
        attr_name = expr[dot_pos+1:].strip()

        # Check if this is a class instance
        if obj_name in env and isinstance(env[obj_name], LipiClassInstance):
            instance = env[obj_name]
            if attr_name in instance.attributes:
                return instance.attributes[attr_name]
            # Also check if it's స్వీయ/self
            if obj_name in ['స్వీయ', 'self']:
                if attr_name in instance.attributes:
                    return instance.attributes[attr_name]

    # Variable lookup
    if expr in env:
        return env[expr]

    raise ValueError(f"తెలియని వ్యక్తీకరణ (unknown expression): {expr}")


def eval_function_call(call_expr, env):
    """Evaluate a function call: func_name(arg1, arg2) or instance.method(arg1, arg2)"""
    paren_pos = call_expr.index('(')
    func_name = call_expr[:paren_pos].strip()
    args_str = call_expr[paren_pos+1:call_expr.rindex(')')].strip()

    # Check if this is a method call on an instance (v3.0)
    if '.' in func_name:
        dot_pos = func_name.index('.')
        obj_name = func_name[:dot_pos].strip()
        method_name = func_name[dot_pos+1:].strip()

        # Check if this is a class instance
        if obj_name in env and isinstance(env[obj_name], LipiClassInstance):
            instance = env[obj_name]
            # Parse arguments
            args = []
            if args_str:
                for arg in split_arguments(args_str):
                    args.append(eval_lipi_expr(arg.strip(), env))
            return call_method(instance, method_name, args, env)

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

    # v3.0: Lipi module import: దిగుమతి func from "module" / import func from "module"
    if line.startswith("దిగుమతి ") or line.startswith("import "):
        # Check if it's a module import (has "from" keyword)
        if " from " in line:
            parse_import_statement(line, runtime, env)
            return
        # Otherwise fall through to other statement types

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

    # Standalone function call: call func(args) or కాల్ func(args)
    if line.startswith('call ') or line.startswith('కాల్ '):
        eval_lipi_expr(line, env)
        return

    # Standalone built-in function calls (file operations, http, db)
    # Check these BEFORE assignment to avoid false positives with '=' in function arguments
    builtin_prefixes = [
        'file_read(', 'file_write(', 'file_append(',
        'ఫైల్_చదువు(', 'ఫైల్_వ్రాయి(', 'ఫైల్_జోడించు(',
        'http_get(', 'http_post(',
        'http_పొందు(', 'http_పంపు(',
        'db_connect(', 'db_query(', 'db_close(',
        'డేటాబేస్_కనెక్ట్(', 'డేటాబేస్_ప్రశ్న(', 'డేటాబేస్_మూసివేయి(',
        'mysql_connect(', 'mysql_query(', 'mysql_close(',  # v3.0 MySQL
        'mysql_కనెక్ట్(', 'mysql_ప్రశ్న(', 'mysql_మూసివేయి(',  # v3.0 MySQL Telugu
        'postgres_connect(', 'postgres_query(', 'postgres_close(',  # v3.0 PostgreSQL
        'postgres_కనెక్ట్(', 'postgres_ప్రశ్న(', 'postgres_మూసివేయి('  # v3.0 PostgreSQL Telugu
    ]
    for prefix in builtin_prefixes:
        if line.startswith(prefix):
            eval_lipi_expr(line, env)
            return

    # Assignment: name = expr
    if "=" in line and not any(op in line for op in ["==", ">=", "<=", "!="]):
        name, expr = line.split("=", 1)
        name = name.strip()
        expr = expr.strip()

        # Attribute assignment: self.name = expr or స్వీయ.name = expr (v3.0)
        if '.' in name:
            dot_pos = name.index('.')
            obj_name = name[:dot_pos].strip()
            attr_name = name[dot_pos+1:].strip()

            # Check if this is a class instance
            if obj_name in env and isinstance(env[obj_name], LipiClassInstance):
                instance = env[obj_name]
                instance.attributes[attr_name] = eval_lipi_expr(expr, env)
                return

        # Regular variable assignment
        env[name] = eval_lipi_expr(expr, env)
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
# Class Definition Parser (v3.0)
# ---------------------------
def parse_class_definition(lines, start_index, env):
    """
    Parse class definition starting at start_index.
    Supports: class ClassName: / క్లాస్ ClassName:
    Returns: (next_index)
    """
    line = lines[start_index].strip()

    # Check for Telugu or English class definition
    is_telugu = line.startswith("క్లాస్ ")
    is_english = line.startswith("class ")

    if not (is_telugu or is_english) or ':' not in line:
        return None

    # Extract class name
    if is_telugu:
        class_decl = line[len("క్లాస్ "):-1].strip()
    else:
        class_decl = line[len("class "):-1].strip()

    # Check for inheritance (not implemented in Day 2, but prepare for Day 3)
    parent_class = None
    if '(' in class_decl:
        paren_pos = class_decl.index('(')
        class_name = class_decl[:paren_pos].strip()
        parent_class = class_decl[paren_pos+1:class_decl.rindex(')')].strip()
    else:
        class_name = class_decl.strip()

    # Collect class body (methods and attributes)
    methods = {}
    i = start_index + 1
    nesting_depth = 0

    while i < len(lines):
        stripped = lines[i].strip()

        # Check if this is a method definition
        if (stripped.startswith("పనిచేయి ") or stripped.startswith("function ")) and stripped.endswith(":"):
            # Parse method definition
            method_result = parse_function_definition(lines, i, env)
            if method_result:
                i = method_result
                # Get the method that was just added to runtime.functions
                # The last added function is the method we just parsed
                last_func_name = list(runtime.functions.keys())[-1]
                method_def = runtime.functions.pop(last_func_name)
                methods[last_func_name] = method_def
                continue

        # Track nested control structures
        if any(stripped.startswith(kw) for kw in ["యెడల", "if", "లేకపోతే", "else",
                                                    "అలాగే", "elif", "ఎప్పుడు", "while",
                                                    "పునరావృతం", "for", "పనిచేయి", "function",
                                                    "ప్రయత్నించు:", "try:"]):
            nesting_depth += 1
        elif stripped in ["ముగింపు", "end"]:
            if nesting_depth == 0:
                # This closes the class
                break
            else:
                # This closes a nested structure
                nesting_depth -= 1

        i += 1

    # Store class in runtime
    runtime.classes[class_name] = {
        'methods': methods,
        'parent': parent_class,
        'env': env.copy()  # Capture closure
    }

    # Return index after 'ముగింపు' or 'end'
    return i + 1


# ---------------------------
# Class Instance Creation (v3.0)
# ---------------------------
class LipiClassInstance:
    """Represents an instance of a Lipi class"""
    def __init__(self, class_name, class_def):
        self.class_name = class_name
        self.class_def = class_def
        self.attributes = {}


def instantiate_class(class_name, args, env):
    """
    Create a new instance of a class.
    Example: person = Person("Ram", 25)
    Supports inheritance: looks up __init__ in child, then parent, then grandparent, etc.
    """
    if class_name not in runtime.classes:
        raise LipiException(f"Undefined class: {class_name}")

    class_def = runtime.classes[class_name]
    instance = LipiClassInstance(class_name, class_def)

    # v3.0: Look for __init__ in class hierarchy (inheritance support)
    init_method = None
    current_class_def = class_def

    while current_class_def is not None:
        if '__init__' in current_class_def['methods']:
            init_method = current_class_def['methods']['__init__']
            break

        # Move to parent class
        parent_name = current_class_def.get('parent')
        if parent_name and parent_name in runtime.classes:
            current_class_def = runtime.classes[parent_name]
        else:
            current_class_def = None

    # Call __init__ if found in hierarchy
    if init_method:
        # Create method environment with self bound to instance
        method_env = env.copy()
        method_env['స్వీయ'] = instance  # Telugu 'self'
        method_env['self'] = instance  # English 'self'

        # Bind parameters
        params = init_method['params']
        if len(args) != len(params) - 1:  # -1 because first param is self
            raise LipiException(f"__init__ expects {len(params)-1} arguments, got {len(args)}")

        # Skip first parameter (self/స్వీయ)
        for i, param_name in enumerate(params[1:]):
            method_env[param_name] = args[i]

        # Execute __init__ body
        try:
            execute_block(init_method['body'], method_env)
        except LipiReturnValue:
            pass  # __init__ shouldn't return values, but handle it gracefully

    return instance


def call_method(instance, method_name, args, env):
    """
    Call a method on a class instance.
    Example: person.greet()
    Supports inheritance: looks up method in child, then parent, then grandparent, etc.
    """
    if not isinstance(instance, LipiClassInstance):
        raise LipiException(f"Cannot call method on non-instance: {type(instance)}")

    # v3.0: Walk inheritance chain to find method
    method = None
    current_class_def = instance.class_def
    method_class_name = instance.class_name

    # Look up method in class hierarchy
    while current_class_def is not None:
        if method_name in current_class_def['methods']:
            method = current_class_def['methods'][method_name]
            break

        # Move to parent class
        parent_name = current_class_def.get('parent')
        if parent_name and parent_name in runtime.classes:
            current_class_def = runtime.classes[parent_name]
            method_class_name = parent_name
        else:
            current_class_def = None

    if method is None:
        raise LipiException(f"Undefined method: {instance.class_name}.{method_name}")

    # Create method environment with self bound to instance
    method_env = env.copy()
    method_env['స్వీయ'] = instance  # Telugu 'self'
    method_env['self'] = instance  # English 'self'

    # Bind parameters (skip first which is self/స్వీయ)
    params = method['params']
    if len(args) != len(params) - 1:  # -1 because first param is self
        raise LipiException(f"{method_name} expects {len(params)-1} arguments, got {len(args)}")

    for i, param_name in enumerate(params[1:]):
        method_env[param_name] = args[i]

    # Execute method body
    try:
        execute_block(method['body'], method_env)
        return None  # Methods that don't return anything
    except LipiReturnValue as ret:
        return ret.value


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

        # Class definition (v3.0)
        if (line.startswith("క్లాస్ ") or line.startswith("class ")) and line.endswith(":"):
            i = parse_class_definition(lines, i, env)
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

    # v3.0: Set current module path for imports
    runtime.current_module_path = os.path.abspath(path)

    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f]

    try:
        execute_block(lines, env)
    except Exception as e:
        print(f"[లోపం] Runtime error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Reset module path
        runtime.current_module_path = None


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
