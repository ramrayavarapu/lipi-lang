# ========================================
# CALCULATOR APP - లిపి కాలిక్యులేటర్
# ========================================
# A comprehensive calculator application demonstrating
# arithmetic operations in lipi-lang
#
# Features:
# - Basic arithmetic (addition, subtraction, multiplication, division)
# - Advanced operations (power, modulo, square root)
# - Error handling for division by zero
# - Bilingual output (English + Telugu)

print "========================================="
print "   LIPI CALCULATOR - లిపి కాలిక్యులేటర్"
print "========================================="
చెప్పు ""

# ========================================
# BASIC ARITHMETIC FUNCTIONS
# ========================================

# Addition Function
function add(a, b):
    return a + b
end

# Subtraction Function
function subtract(a, b):
    return a - b
end

# Multiplication Function
function multiply(a, b):
    return a * b
end

# Division Function with error handling
function divide(a, b):
    if b == 0:
        print "❌ Error: Division by zero is not allowed!"
        చెప్పు "❌ దోషం: సున్నాతో భాగించలేము!"
        return null
    end
    return a / b
end

# Modulo Function (Remainder)
function modulo(a, b):
    if b == 0:
        print "❌ Error: Modulo by zero is not allowed!"
        చెప్పు "❌ దోషం: సున్నాతో మాడ్యులో చేయలేము!"
        return null
    end
    return a % b
end

# Power Function (a raised to power b)
function power(a, b):
    return a ** b
end

# Square Root Function (approximate)
function square_root(n):
    if n < 0:
        print "❌ Error: Cannot calculate square root of negative number!"
        చెప్పు "❌ దోషం: ప్రతికూల సంఖ్య యొక్క వర్గమూలం లెక్కించలేము!"
        return null
    end

    # Using Newton's method for square root approximation
    if n == 0:
        return 0
    end

    if n == 1:
        return 1
    end

    guess = n / 2
    precision = 0.00001
    iterations = 0
    max_iterations = 100

    while iterations < max_iterations:
        # Newton's method: better_guess = (guess + n/guess) / 2
        n_div_guess = n / guess
        sum_val = guess + n_div_guess
        better_guess = sum_val / 2

        # Calculate difference
        diff = guess - better_guess

        if diff < 0:
            diff = diff * -1
        end

        if diff < precision:
            return better_guess
        end

        guess = better_guess
        iterations = iterations + 1
    end

    return guess
end

# ========================================
# CALCULATOR DEMONSTRATIONS
# ========================================

print ""
print "📊 BASIC ARITHMETIC OPERATIONS"
print "================================"
చెప్పు ""

# Test values
num1 = 25
num2 = 5

# Addition
result = కాల్ add(num1, num2)
n1_str = str(num1)
n2_str = str(num2)
res_str = str(result)
print "➕ Addition: " + n1_str + " + " + n2_str + " = " + res_str
చెప్పు "➕ కూడిక: " + n1_str + " + " + n2_str + " = " + res_str
చెప్పు ""

# Subtraction
result = కాల్ subtract(num1, num2)
res_str = str(result)
print "➖ Subtraction: " + n1_str + " - " + n2_str + " = " + res_str
చెప్పు "➖ వ్యవకలనం: " + n1_str + " - " + n2_str + " = " + res_str
చెప్పు ""

# Multiplication
result = కాల్ multiply(num1, num2)
res_str = str(result)
print "✖️  Multiplication: " + n1_str + " × " + n2_str + " = " + res_str
చెప్పు "✖️  గుణకారం: " + n1_str + " × " + n2_str + " = " + res_str
చెప్పు ""

# Division
result = కాల్ divide(num1, num2)
res_str = str(result)
print "➗ Division: " + n1_str + " ÷ " + n2_str + " = " + res_str
చెప్పు "➗ భాగహారం: " + n1_str + " ÷ " + n2_str + " = " + res_str
చెప్పు ""

# ========================================
# ADVANCED OPERATIONS
# ========================================

print ""
print "🔬 ADVANCED OPERATIONS"
print "======================"
చెప్పు ""

# Power operation
base = 2
exponent = 10
result = కాల్ power(base, exponent)
base_str = str(base)
exp_str = str(exponent)
res_str = str(result)
print "⚡ Power: " + base_str + " ^ " + exp_str + " = " + res_str
చెప్పు "⚡ ఘాతాంకం: " + base_str + " ^ " + exp_str + " = " + res_str
చెప్పు ""

# Modulo operation
result = కాల్ modulo(num1, num2)
res_str = str(result)
print "📐 Modulo: " + n1_str + " % " + n2_str + " = " + res_str
చెప్పు "📐 మాడ్యులో: " + n1_str + " % " + n2_str + " = " + res_str
చెప్పు ""

# Square root
number = 144
result = కాల్ square_root(number)
num_str = str(number)
res_str = str(result)
print "√  Square Root: √" + num_str + " = " + res_str
చెప్పు "√  వర్గమూలం: √" + num_str + " = " + res_str
చెప్పు ""

# ========================================
# COMPLEX CALCULATIONS
# ========================================

print ""
print "🧮 COMPLEX CALCULATIONS"
print "======================="
చెప్పు ""

# Example: Calculate area of a circle (πr²)
# Using π ≈ 3.14159
pi = 3.14159
radius = 7

# Calculate r²
r_squared = కాల్ power(radius, 2)
# Calculate π × r²
area = కాల్ multiply(pi, r_squared)

radius_str = str(radius)
pi_str = str(pi)
area_str = str(area)

print "🔵 Area of circle with radius " + radius_str + ":"
print "   A = π × r² = " + pi_str + " × " + radius_str + "² = " + area_str
చెప్పు "🔵 వ్యాసార్థం " + radius_str + " ఉన్న వృత్తం యొక్క వైశాల్యం:"
చెప్పు "   A = π × r² = " + pi_str + " × " + radius_str + "² = " + area_str
చెప్పు ""

# Example: Quadratic expression evaluation (ax² + bx + c)
a = 2
b = 5
c = 3
x = 4

# Calculate ax²
x_squared = కాల్ power(x, 2)
term1 = కాల్ multiply(a, x_squared)

# Calculate bx
term2 = కాల్ multiply(b, x)

# Calculate ax² + bx
temp = కాల్ add(term1, term2)

# Calculate ax² + bx + c
result = కాల్ add(temp, c)

a_str = str(a)
b_str = str(b)
c_str = str(c)
x_str = str(x)
res_str = str(result)

print "📈 Quadratic Expression: " + a_str + "x² + " + b_str + "x + " + c_str + " where x = " + x_str
print "   Result: " + a_str + "×" + x_str + "² + " + b_str + "×" + x_str + " + " + c_str + " = " + res_str
చెప్పు "📈 వర్గ సమీకరణం: " + a_str + "x² + " + b_str + "x + " + c_str + " where x = " + x_str
చెప్పు "   ఫలితం: " + a_str + "×" + x_str + "² + " + b_str + "×" + x_str + " + " + c_str + " = " + res_str
చెప్పు ""

# ========================================
# ERROR HANDLING DEMONSTRATIONS
# ========================================

print ""
print "⚠️  ERROR HANDLING"
print "=================="
చెప్పు ""

# Division by zero
print "Testing division by zero:"
చెప్పు "సున్నాతో భాగించడం పరీక్ష:"
result = కాల్ divide(10, 0)
చెప్పు ""

# Square root of negative number
print "Testing square root of negative number:"
చెప్పు "ప్రతికూల సంఖ్య యొక్క వర్గమూలం పరీక్ష:"
result = కాల్ square_root(-16)
చెప్పు ""

# ========================================
# BATCH CALCULATIONS
# ========================================

print ""
print "📋 BATCH CALCULATIONS"
print "====================="
చెప్పు ""

# Calculate factorials approximation using power
print "Powers of 2 (2^n):"
చెప్పు "2 యొక్క ఘాతాంకాలు (2^n):"

n = 0
వరకు n <= 10:
    result = కాల్ power(2, n)
    n_str = str(n)
    res_str = str(result)
    print "2^" + n_str + " = " + res_str
    n = n + 1
ముగింపు

చెప్పు ""

# Calculate squares of numbers
print "Perfect Squares (n²):"
చెప్పు "పరిపూర్ణ వర్గాలు (n²):"

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
పునరావృతం num in numbers:
    square = కాల్ power(num, 2)
    root = కాల్ square_root(square)
    num_str = str(num)
    sq_str = str(square)
    root_str = str(root)
    print num_str + "² = " + sq_str + " (√" + sq_str + " = " + root_str + ")"
ముగింపు

# ========================================
# SUMMARY
# ========================================

print ""
print "========================================="
print "   ✅ CALCULATOR OPERATIONS COMPLETED"
print "   ✅ కాలిక్యులేటర్ కార్యకలాపాలు పూర్తయ్యాయి"
print "========================================="
చెప్పు ""
print "Thank you for using Lipi Calculator!"
చెప్పు "లిపి కాలిక్యులేటర్ ఉపయోగించినందుకు ధన్యవాదాలు!"
