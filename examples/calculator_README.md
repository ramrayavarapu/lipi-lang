# LIPI CALCULATOR - లిపి కాలిక్యులేటర్

A comprehensive calculator application built with lipi-lang, demonstrating bilingual programming capabilities in Telugu and English.

## Overview

The Lipi Calculator is a feature-rich calculator application that showcases the power of lipi-lang's bilingual programming features. It performs basic arithmetic operations, advanced mathematical calculations, and includes robust error handling.

## Features

### 📊 Basic Arithmetic Operations
- **Addition** (కూడిక) - Add two numbers
- **Subtraction** (వ్యవకలనం) - Subtract two numbers
- **Multiplication** (గుణకారం) - Multiply two numbers
- **Division** (భాగహారం) - Divide two numbers with zero-division protection

### 🔬 Advanced Operations
- **Power** (ఘాతాంకం) - Calculate exponents (a^b)
- **Modulo** (మాడ్యులో) - Calculate remainder (a % b)
- **Square Root** (వర్గమూలం) - Calculate square roots using Newton's method

### 🧮 Complex Calculations
- **Circle Area** - Calculate area using πr²
- **Quadratic Expressions** - Evaluate polynomial expressions (ax² + bx + c)
- **Batch Processing** - Calculate powers of 2 and perfect squares

### ⚠️ Error Handling
- Division by zero protection
- Negative square root detection
- User-friendly bilingual error messages

## How to Run

```bash
# Navigate to the lipi-lang directory
cd /path/to/lipi-lang

# Run the calculator
python3 src/lipi.py examples/calculator.lipi.py
```

## Sample Output

```
=========================================
   LIPI CALCULATOR - లిపి కాలిక్యులేటర్
=========================================

📊 BASIC ARITHMETIC OPERATIONS
================================

➕ Addition: 25 + 5 = 30
➕ కూడిక: 25 + 5 = 30

➖ Subtraction: 25 - 5 = 20
➖ వ్యవకలనం: 25 - 5 = 20

✖️  Multiplication: 25 × 5 = 125
✖️  గుణకారం: 25 × 5 = 125

➗ Division: 25 ÷ 5 = 5.0
➗ భాగహారం: 25 ÷ 5 = 5.0
```

## Code Structure

### Function Definitions

```python
# Addition Function
function add(a, b):
    return a + b
end

# Subtraction Function
function subtract(a, b):
    return a - b
end

# Division with Error Handling
function divide(a, b):
    if b == 0:
        print "❌ Error: Division by zero is not allowed!"
        చెప్పు "❌ దోషం: సున్నాతో భాగించలేము!"
        return null
    end
    return a / b
end
```

### Telugu Keywords Used

- `కాల్` - Call function (call)
- `చెప్పు` - Print/Say (print)
- `యెడల` - If (if)
- `లేకపోతే` - Else (else)
- `వరకు` - While (while)
- `పునరావృతం` - For loop (for)
- `ముగింపు` - End block (end)
- `రిటర్న్` - Return (return)
- `పనిచేయి` - Function definition (function)

## Mathematical Algorithms

### Square Root (Newton's Method)

The calculator implements Newton's method for square root approximation:

```
better_guess = (guess + n/guess) / 2
```

This iterative method converges quickly to the accurate square root value with a precision of 0.00001.

### Quadratic Expression Evaluation

Evaluates expressions of the form: **ax² + bx + c**

Example: For a=2, b=5, c=3, x=4:
- Calculate: 2×4² + 5×4 + 3 = 2×16 + 20 + 3 = 32 + 20 + 3 = **55**

## Educational Value

This calculator demonstrates:

1. **Bilingual Programming** - Mixing Telugu and English seamlessly
2. **Function Definition** - Creating reusable functions
3. **Control Flow** - Using if/else, while, and for loops
4. **Error Handling** - Graceful handling of edge cases
5. **Mathematical Algorithms** - Implementing Newton's method
6. **Code Organization** - Structured, readable code

## Extensibility

You can easily extend the calculator by adding:

- **Trigonometric functions** (sin, cos, tan)
- **Logarithmic operations** (log, ln)
- **Factorial calculations**
- **Scientific notation support**
- **User input** (using Python modules)

## Requirements

- Python 3.6 or higher
- lipi-lang interpreter (`src/lipi.py`)

## Language Version

Built for **lipi-lang v2.0** - Production-ready bilingual programming language

## License

Part of the lipi-lang project - enabling Telugu students to learn programming in their native language.

## Credits

Developed as a demonstration of lipi-lang's capabilities for building practical applications with bilingual programming support.

---

**Happy Calculating! / లెక్కలు సంతోషంగా ఉండండి!** 🧮
