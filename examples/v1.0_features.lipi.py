# lipi-lang v1.0 Feature Demonstration
# Comprehensive example showing all new features
# ================================================

చెప్పు "=== lipi-lang v1.0 Features Demo ==="
చెప్పు ""

# ================================================
# 1. FUNCTIONS / పనులు
# ================================================
చెప్పు "1. Functions Example:"

# Telugu function
పనిచేయి జోడించు(a, b):
    result = a + b
    రిటర్న్ result
ముగింపు

# English function
function multiply(x, y):
    product = x * y
    return product
end

# Call functions
sum_result = కాల్ జోడించు(10, 20)
చెప్పు "10 + 20 = " + str(sum_result)

product_result = call multiply(5, 7)
print "5 × 7 = " + str(product_result)
చెప్పు ""

# ================================================
# 2. ARRAYS / జాబితాలు
# ================================================
చెప్పు "2. Arrays Example:"

# Create arrays
numbers = [1, 2, 3, 4, 5]
names = ["Ram", "Sita", "Lakshman"]

చెప్పు "Numbers: " + str(numbers)
చెప్పు "Names: " + str(names)

# Array indexing
first_number = numbers[0]
చెప్పు "First number: " + str(first_number)

second_name = names[1]
print "Second name: " + second_name

# Array length
length = len(numbers)
చెప్పు "Array length: " + str(length)
చెప్పు ""

# ================================================
# 3. OBJECTS / వస్తువులు
# ================================================
చెప్పు "3. Objects Example:"

# Create object
person = {"name": "Ram", "age": 25, "city": "Hyderabad"}
చెప్పు "Person: " + str(person)

# Access properties
name = person["name"]
చెప్పు "Name: " + name

age = person["age"]
print "Age: " + str(age)
చెప్పు ""

# ================================================
# 4. FOR LOOPS / పునరావృత చక్రాలు
# ================================================
చెప్పు "4. For Loops Example:"

# Telugu for loop
చెప్పు "Counting in Telugu:"
numbers_list = [1, 2, 3, 4, 5]
పునరావృతం num in numbers_list:
    చెప్పు "సంఖ్య: " + str(num)
ముగింపు

# English for loop
print "Iterating through names:"
name_list = ["Alice", "Bob", "Charlie"]
for name in name_list:
    print "Name: " + name
end
చెప్పు ""

# ================================================
# 5. PYTHON LIBRARY ACCESS / Python లైబ్రరీ యాక్సెస్
# ================================================
చెప్పు "5. Python Library Access Example:"

# Import Python's math module
దిగుమతి_python("math")

# Use math functions
square_root = math.sqrt(16)
చెప్పు "Square root of 16: " + str(square_root)

power = math.pow(2, 8)
print "2^8 = " + str(power)

pi_value = math.pi
చెప్పు "Value of π: " + str(pi_value)
చెప్పు ""

# Import datetime
import_python("datetime")

# Get current year (simplified - datetime access would need enhancement)
చెప్పు "Python libraries imported successfully!"
చెప్పు ""

# ================================================
# 6. ERROR HANDLING / దోష నిర్వహణ
# ================================================
చెప్పు "6. Error Handling Example:"

# Try-catch in Telugu
ప్రయత్నించు:
    risky = 10 / 2
    చెప్పు "Division successful: " + str(risky)
పట్టుకో:
    చెప్పు "Error occurred in Telugu try-catch"
చివరకు:
    చెప్పు "Telugu try-catch completed"
ముగింపు

# Try-catch in English
try:
    safe = 100 / 4
    print "Safe division: " + str(safe)
catch:
    print "Error in English try-catch"
finally:
    print "English try-catch completed"
end
చెప్పు ""

# ================================================
# 7. NESTED STRUCTURES / సంకీర్ణ నిర్మాణాలు
# ================================================
చెప్పు "7. Nested Structures Example:"

# Function with if-else and for loop
పనిచేయి print_even_numbers(nums):
    print "Even numbers:"
    పునరావృతం n in nums:
        యెడల n % 2 == 0:
            చెప్పు "  " + str(n)
        ముగింపు
    ముగింపు
ముగింపు

test_numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
call print_even_numbers(test_numbers)
చెప్పు ""

# ================================================
# 8. BOOLEAN & NULL / బూలియన్ & శూన్యం
# ================================================
చెప్పు "8. Boolean and Null Example:"

# Boolean literals
is_valid = true
is_error = false
చెప్పు "Is valid? " + str(is_valid)
print "Is error? " + str(is_error)

# Telugu boolean
తెలుగు_నిజం = నిజం
తెలుగు_అబద్ధం = అబద్ధం
చెప్పు "Telugu true: " + str(తెలుగు_నిజం)

# Null handling
empty_value = null
యెడల empty_value == null:
    చెప్పు "Value is null"
ముగింపు
చెప్పు ""

# ================================================
# 9. ENHANCED OPERATORS / మెరుగైన ఆపరేటర్లు
# ================================================
చెప్పు "9. Enhanced Operators Example:"

a = 10
b = 3

# Subtraction
difference = a - b
చెప్పు "10 - 3 = " + str(difference)

# Multiplication
product = a * b
print "10 × 3 = " + str(product)

# Division
quotient = a / b
చెప్పు "10 ÷ 3 = " + str(quotient)

# Modulus
remainder = a % b
print "10 % 3 = " + str(remainder)

# Power
power_val = 2 ** 10
చెప్పు "2^10 = " + str(power_val)
చెప్పు ""

# ================================================
# 10. BILINGUAL COLLABORATION / ద్విభాషా సహకారం
# ================================================
చెప్పు "10. Bilingual Collaboration Example:"

# Telugu developer creates a function
పనిచేయి calculate_total(items):
    total = 0
    పునరావృతం item in items:
        total = total + item
    ముగింపు
    return total
ముగింపు

# English developer uses it
shopping_cart = [100, 250, 75, 300]
cart_total = call calculate_total(shopping_cart)
print "Shopping cart total: ₹" + str(cart_total)

# Mixed language control flow
యెడల cart_total > 500:
    print "Eligible for free shipping!"
లేకపోతే:
    యెడల cart_total > 200:
        చెప్పు "10% discount applied"
    లేకపోతే:
        print "Add more items for discount"
    ముగింపు
ముగింపు

చెప్పు ""
చెప్పు "=== All v1.0 Features Demonstrated Successfully! ==="
చెప్పు "lipi-lang is now production-ready! 🎉"
