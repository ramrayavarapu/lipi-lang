# Lipi Language v3.0 Developer Guide
## Complete Guide to Enterprise Features

**lipi-lang v3.0** is an enterprise-ready bilingual (Telugu + English) programming language that supports modules, object-oriented programming, and multi-database connectivity.

---

## Table of Contents

1. [Module System](#module-system)
2. [Object-Oriented Programming](#object-oriented-programming)
3. [Multi-Database Support](#multi-database-support)
4. [Bilingual Programming](#bilingual-programming)
5. [Best Practices](#best-practices)
6. [Migration Guide](#migration-guide)

---

## Module System

### Overview

The module system allows you to organize code across multiple files, enabling better code reuse and maintainability.

### Basic Usage

**Creating a Module:**

```python
# File: utils.lipi.py
పనిచేయి greet(name):
    రిటర్న్ "Hello, " + name
ముగింపు

function calculate(a, b):
    return a + b
end

# Export functions for use in other files
ఎగుమతి greet, calculate
```

**Importing a Module:**

```python
# File: main.lipi.py
దిగుమతి greet, calculate from "utils"

result = కాల్ greet("Ram")
sum = call calculate("10", "20")
```

### Features

- **Module Caching**: Modules are loaded once and cached for performance
- **Circular Import Detection**: Prevents infinite loops from circular dependencies
- **Path Security**: Blocks path traversal attacks (`../` patterns)
- **Bilingual Support**: Use తెలుగు or English keywords interchangeably

### Advanced Examples

**Multiple Imports:**

```python
దిగుమతి func1, func2, func3 from "my_module"
import var1, var2 from "another_module"
```

**Organizing Code:**

```
project/
  ├── main.lipi.py
  ├── models/
  │   ├── user.lipi.py
  │   └── product.lipi.py
  └── utils/
      └── helpers.lipi.py
```

---

## Object-Oriented Programming

### Overview

v3.0 introduces full object-oriented programming with classes, inheritance, and method overriding.

### Basic Class Definition

**Telugu Syntax:**

```python
క్లాస్ Person:
    పనిచేయి __init__(స్వీయ, name, age):
        స్వీయ.name = name
        స్వీయ.age = age
    ముగింపు

    పనిచేయి greet(స్వీయ):
        చెప్పు "నమస్తే, నేను " + స్వీయ.name
    ముగింపు
ముగింపు

# Create an instance
person = Person("రాము", "25")
కాల్ person.greet()
```

**English Syntax:**

```python
class Person:
    function __init__(self, name, age):
        self.name = name
        self.age = age
    end

    function greet(self):
        print "Hello, I am " + self.name
    end
end

# Create an instance
person = Person("Ram", "25")
call person.greet()
```

### Instance Variables

Instance variables are accessed using `self` (English) or `స్వీయ` (Telugu):

```python
class Counter:
    function __init__(self, start):
        self.count = start
    end

    function increment(self):
        self.count = self.count + "1"
        return self.count
    end
end

counter = Counter("0")
new_value = call counter.increment()
```

### Inheritance

**Simple Inheritance:**

```python
# Parent class
class Animal:
    function __init__(self, name):
        self.name = name
    end

    function speak(self):
        return "Some sound"
    end
end

# Child class
class Dog(Animal):
    function speak(self):
        return "Bark!"  # Overrides parent method
    end
end

dog = Dog("Buddy")
sound = call dog.speak()  # Returns "Bark!"
```

**Multi-Level Inheritance:**

```python
క్లాస్ LivingThing:
    పనిచేయి breathe(స్వీయ):
        చెప్పు "Breathing..."
    ముగింపు
ముగింపు

క్లాస్ Mammal(LivingThing):
    పనిచేయి feed_young(స్వీయ):
        చెప్పు "Feeding with milk"
    ముగింపు
ముగింపు

క్లాస్ Dog(Mammal):
    పనిచేయి bark(స్వీయ):
        చెప్పు "Woof!"
    ముగింపు
ముగింపు

dog = Dog()
కాల్ dog.breathe()      # From grandparent
కాల్ dog.feed_young()   # From parent
కాల్ dog.bark()         # Own method
```

### Method Overriding

Child classes can override parent methods:

```python
class Shape:
    function area(self):
        return "0"
    end
end

class Circle(Shape):
    function __init__(self, radius):
        self.radius = radius
    end

    function area(self):
        # Overrides parent's area() method
        return self.radius + " x " + self.radius
    end
end
```

### Constructor Inheritance

If a child class doesn't define `__init__`, it uses the parent's:

```python
క్లాస్ Base:
    పనిచేయి __init__(స్వీయ, value):
        స్వీయ.value = value
    ముగింపు
ముగింపు

క్లాస్ Derived(Base):
    # No __init__ defined, uses parent's
    పనిచేయి show(స్వీయ):
        చెప్పు స్వీయ.value
    ముగింపు
ముగింపు

obj = Derived("test")  # Uses Base's __init__
```

---

## Multi-Database Support

### Overview

Lipi v3.0 supports three database backends:
- **SQLite**: Lightweight, file-based (v2.0+)
- **MySQL**: Enterprise-scale relational database (v3.0+)
- **PostgreSQL**: Advanced enterprise database (v3.0+)

### SQLite (Built-in)

**Basic Usage:**

```python
# Connect to database
db = db_connect("myapp.db")

# Create table
db_query(db, "CREATE TABLE users (id INTEGER, name TEXT)")

# Insert data
db_query(db, "INSERT INTO users VALUES (?, ?)", [1, "Ram"])

# Query data
users = db_query(db, "SELECT * FROM users")

# Close connection
db_close(db)
```

**Telugu Syntax:**

```python
డేటాబేస్ = డేటాబేస్_కనెక్ట్("myapp.db")
డేటాబేస్_ప్రశ్న(డేటాబేస్, "CREATE TABLE ...")
డేటాబేస్_మూసివేయి(డేటాబేస్)
```

### MySQL (v3.0)

**Installation:**

```bash
pip install mysql-connector-python
```

**Usage:**

```python
# Connect (host, user, password, database)
mysql_db = mysql_connect("localhost", "user", "password", "shop_db")

# Create table
mysql_query(mysql_db, "CREATE TABLE products (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), price DECIMAL(10,2))")

# Insert with parameterized query (prevents SQL injection)
mysql_query(mysql_db, "INSERT INTO products (name, price) VALUES (%s, %s)", ["Laptop", 50000])

# Query data
products = mysql_query(mysql_db, "SELECT * FROM products")

# Iterate results (returned as dictionaries)
పునరావృతం product in products:
    చెప్పు product["name"] + ": ₹" + product["price"]
ముగింపు

# Close connection
mysql_close(mysql_db)
```

**Telugu Syntax:**

```python
డేటాబేస్ = mysql_కనెక్ట్("localhost", "user", "password", "db")
mysql_ప్రశ్న(డేటాబేస్, "SELECT * FROM users")
mysql_మూసివేయి(డేటాబేస్)
```

### PostgreSQL (v3.0)

**Installation:**

```bash
pip install psycopg2-binary
```

**Usage:**

```python
# Connect (host, user, password, database, [port])
pg_db = postgres_connect("localhost", "user", "password", "analytics_db", "5432")

# Create table with SERIAL (PostgreSQL feature)
postgres_query(pg_db, "CREATE TABLE events (id SERIAL PRIMARY KEY, name VARCHAR(100), timestamp TIMESTAMP)")

# Insert with RETURNING clause (PostgreSQL feature)
result = postgres_query(pg_db, "INSERT INTO events (name) VALUES (%s) RETURNING id", ["UserLogin"])
new_id = result[0]["id"]

# Query data
events = postgres_query(pg_db, "SELECT * FROM events ORDER BY timestamp DESC")

# Close connection
postgres_close(pg_db)
```

**Telugu Syntax:**

```python
డేటాబేస్ = postgres_కనెక్ట్("localhost", "user", "pass", "db")
postgres_ప్రశ్న(డేటాబేస్, "SELECT * FROM users")
postgres_మూసివేయి(డేటాబేస్)
```

### Security: Parameterized Queries

**Always use parameterized queries to prevent SQL injection:**

```python
# ✅ SAFE - Parameterized query
user_input = "Ram"
db_query(db, "SELECT * FROM users WHERE name = ?", [user_input])

# ❌ UNSAFE - String concatenation
# db_query(db, "SELECT * FROM users WHERE name = '" + user_input + "'")
```

### Multi-Database Architecture

Use different databases for different purposes:

```python
# SQLite for local/development
local_db = db_connect("local.db")

# MySQL for transactional data
transaction_db = mysql_connect("prod-mysql", "user", "pass", "transactions")

# PostgreSQL for analytics
analytics_db = postgres_connect("prod-pg", "user", "pass", "analytics")

# Use each for its strength
db_query(local_db, "INSERT INTO cache ...")
mysql_query(transaction_db, "INSERT INTO orders ...")
postgres_query(analytics_db, "INSERT INTO events ...")
```

---

## Bilingual Programming

### Overview

Lipi allows seamless mixing of Telugu (తెలుగు) and English keywords in the same program.

### Keyword Equivalents

| English | Telugu | Purpose |
|---------|--------|---------|
| `print` | `చెప్పు` | Output |
| `if` | `యెడల` | Conditional |
| `else` | `లేకపోతే` | Alternative |
| `elif` | `అలాగే` | Else-if |
| `while` | `వరకు` / `ఎప్పుడు` | Loop |
| `for` | `పునరావృతం` | For loop |
| `function` | `పనిచేయి` | Function definition |
| `return` | `రిటర్న్` | Return value |
| `end` | `ముగింపు` | Block end |
| `class` | `క్లాస్` | Class definition |
| `self` | `స్వీయ` | Instance reference |
| `import` | `దిగుమతి` | Import module |
| `export` | `ఎగుమతి` | Export from module |
| `call` | `కాల్` | Function call |
| `true` | `నిజం` | Boolean true |
| `false` | `అబద్ధం` | Boolean false |
| `null` | `శూన్యం` | Null value |

### Mixed Language Examples

**Functions:**

```python
పనిచేయి telugu_function():
    return "Telugu function"
ముగింపు

function english_function():
    రిటర్న్ "Mixed return"
end
```

**Classes:**

```python
class EnglishBase:
    function method(self):
        చెప్పు "Mixed method"
    end
end

క్లాస్ TeluguDerived(EnglishBase):
    పనిచేయి another(స్వీయ):
        print "Another mixed method"
    ముగింపు
end
```

**Control Flow:**

```python
యెడల x == "10":
    print "Equal to 10"
లేకపోతే:
    చెప్పు "Not equal"
ముగింపు
```

---

## Best Practices

### 1. Module Organization

```
project/
  ├── main.lipi.py          # Entry point
  ├── config.lipi.py        # Configuration
  ├── models/               # Data models
  │   ├── user.lipi.py
  │   └── product.lipi.py
  ├── services/             # Business logic
  │   └── auth.lipi.py
  └── utils/                # Utilities
      └── helpers.lipi.py
```

### 2. Use Parameterized Queries

```python
# Always use parameterized queries for database operations
mysql_query(db, "INSERT INTO users VALUES (%s, %s)", [name, email])
```

### 3. Class Design

```python
# Use inheritance for code reuse
క్లాస్ BaseModel:
    పనిచేయి save(స్వీయ, db):
        # Common save logic
    ముగింపు
ముగింపు

క్లాస్ User(BaseModel):
    # User-specific methods
ముగింపు
```

### 4. Error Handling

```python
ప్రయత్నించు:
    db = mysql_connect("localhost", "user", "pass", "db")
పట్టుకో:
    print "Connection failed"
ముగింపు
```

### 5. Consistent Naming

Choose either Telugu or English for your project and be consistent:

```python
# Telugu style
క్లాస్ వినియోగదారు:
    పనిచేయి దొరకు(స్వీయ):
        # ...
    ముగింపు
ముగింపు

# OR English style
class User:
    function find(self):
        # ...
    end
end
```

---

## Migration Guide

### From v2.0 to v3.0

**New Features Available:**

1. **Module System**: Organize code across files
2. **OOP**: Classes and inheritance
3. **MySQL**: Enterprise database support
4. **PostgreSQL**: Advanced database support

**Changes Required:**

None! v3.0 is fully backward compatible with v2.0 code.

**Recommended Upgrades:**

1. **Refactor into modules** for better organization
2. **Convert to classes** for complex data structures
3. **Use MySQL/PostgreSQL** for production databases

**Example Migration:**

**Before (v2.0):**

```python
# All in one file
function create_user(name, email):
    db = db_connect("users.db")
    db_query(db, "INSERT INTO users VALUES (?, ?)", [name, email])
    db_close(db)
end
```

**After (v3.0):**

```python
# models/user.lipi.py
క్లాస్ User:
    పనిచేయి __init__(స్వీయ, name, email):
        స్వీయ.name = name
        స్వీయ.email = email
    ముగింపు

    పనిచేయి save(స్వీయ, db):
        mysql_query(db, "INSERT INTO users VALUES (%s, %s)",
                   [స్వీయ.name, స్వీయ.email])
    ముగింపు
ముగింపు

ఎగుమతి User

# main.lipi.py
దిగుమతి User from "models/user"

db = mysql_connect("localhost", "root", "pass", "myapp")
user = User("రాము", "ram@example.com")
కాల్ user.save(db)
mysql_close(db)
```

---

## Complete Example

See `examples/v3.0_enterprise_example.lipi.py` for a complete e-commerce application demonstrating all v3.0 features.

---

## Resources

- **GitHub**: [lipi-lang repository](https://github.com/ramrayavarapu/lipi-lang)
- **Examples**: See `examples/` directory
- **Tests**: See `tests/` directory for usage examples
- **Security**: See `docs/SECURITY.md`

---

## FAQ

**Q: Can I mix Telugu and English in the same file?**
A: Yes! Lipi fully supports bilingual programming.

**Q: Which database should I use?**
A: SQLite for small apps, MySQL for transactions, PostgreSQL for analytics.

**Q: Does inheritance work across languages?**
A: Yes! Telugu classes can inherit from English classes and vice versa.

**Q: Are my databases secure?**
A: Yes, when using parameterized queries. Always use `[params]` arrays.

**Q: Can I use Python libraries?**
A: Yes, via `దిగుమతి_python` / `import_python` (from v1.0).

---

**Lipi v3.0 - Enterprise Ready! 🚀**
