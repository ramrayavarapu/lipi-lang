# v3.0 Module Import Test
# Testing the new module import system

చెప్పు "=== v3.0 Module Import System Test ==="
print ""

# Test 1: Import Telugu function
చెప్పు "Test 1: Importing Telugu function..."
దిగుమతి greet_telugu from "v3.0_module_utils"

result = కాల్ greet_telugu("రాము")
చెప్పు "Result: " + result
print ""

# Test 2: Import English function
print "Test 2: Importing English function..."
import greet_english from "v3.0_module_utils"

result2 = call greet_english("John")
print "Result: " + result2
చెప్పు ""

# Test 3: Import multiple items
చెప్పు "Test 3: Importing multiple items..."
దిగుమతి add_numbers, message from "v3.0_module_utils"

sum = కాల్ add_numbers(10, 20)
print "10 + 20 = " + sum
చెప్పు "Message from module: " + message
print ""

# Test 4: Use imported functions in expressions
చెప్పు "Test 4: Using imported functions..."
greeting1 = కాల్ greet_telugu("సీత")
greeting2 = call greet_english("Mary")
చెప్పు greeting1
print greeting2
చెప్పు ""

చెప్పు "=== All Module Tests Passed! ==="
print "✅ Module import system working correctly!"
చెప్పు "✅ దిగుమతి వ్యవస్థ సరిగ్గా పని చేస్తోంది!"
