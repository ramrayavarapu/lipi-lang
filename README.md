# lipi-lang
The bilingual (Telugu + English) programming language.

## Overview

Lipi is a programming language designed to enable Telugu-speaking students to learn programming in their native language, while also supporting English. The unique feature of Lipi is that **Telugu and English can be used together in the same program**, making it easy to transition between languages and collaborate with others.

## Features

✅ **Three Ways to Code:**
1. **Pure Telugu** - Write entirely in Telugu
2. **Pure English** - Write entirely in English
3. **Bilingual** - Mix Telugu and English keywords in the same program!

✅ **Language Support:**

| Feature | Telugu | English |
|---------|--------|---------|
| Print | `చెప్పు` | `print` |
| If | `యెడల` | `if` |
| Else | `లేకపోతే:` | `else:` |
| While | `వరకు` | `while` |
| End block | `ముగింపు` | `end` |

## Quick Start

### Installation

```bash
git clone https://github.com/ramrayavarapu/lipi-lang.git
cd lipi-lang
```

### Running Programs

```bash
# Run a Telugu program
python3 lipi.py examples/hello.lipi.py

# Run an English program
python3 lipi.py examples/english.lipi.py

# Run a bilingual program
python3 lipi.py examples/bilingual.lipi.py

# Start the interactive REPL
python3 lipi.py
```

## Examples

### Telugu Example
```python
పేరు = "రామ్"
వయసు = 20

చెప్పు "నమస్తే!"
చెప్పు "పేరు: " + పేరు

యెడల వయసు > 18:
    చెప్పు "అడల్ట్"
లేకపోతే:
    చెప్పు "యంగ్"
ముగింపు
```

### English Example
```python
name = "John"
age = 20

print "Hello!"
print "Name: " + name

if age > 18:
    print "Adult"
else:
    print "Young"
end
```

### Bilingual Example (Telugu + English Together!)
```python
# Mix Telugu and English freely!
పేరు = "రామ్"
name = "Ram"

చెప్పు "నమస్తే!"
print "Hello!"

# Telugu if with English print inside
యెడల వయసు > 18:
    print "Adult"
ముగింపు

# English while with Telugu print inside
while count < 5:
    చెప్పు "Count: " + count
    count = count + 1
end
```

## Language Syntax

### Variables
```python
పేరు = "value"    # Telugu variable
name = "value"     # English variable
వయసు = 25         # Number
```

### Print Statements
```python
చెప్పు "నమస్తే"     # Telugu print
print "Hello"        # English print
```

### Conditionals
```python
# Telugu
యెడల condition:
    # statements
లేకపోతే:
    # statements
ముగింపు

# English
if condition:
    # statements
else:
    # statements
end
```

### Loops
```python
# Telugu
వరకు condition:
    # statements
ముగింపు

# English
while condition:
    # statements
end
```

## Why Bilingual?

1. **Accessibility** - Telugu students can learn programming in their native language
2. **Transition** - Easy to transition to English-based programming languages
3. **Collaboration** - Mix languages based on what makes sense for your team
4. **Learning** - Understand programming concepts first, language second

## Current Version

**v0.5** - Bilingual support with Telugu and English keywords

## Roadmap

- [ ] Functions/procedures
- [ ] Nested control structures
- [ ] More operators
- [ ] File I/O
- [ ] Standard library
- [ ] More Indian language support (Hindi, Tamil, etc.)

## Contributing

We welcome contributions! This project aims to make programming accessible to non-English speakers.

## License

MIT License
