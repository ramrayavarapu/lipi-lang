# Bilingual Error Message Demo
# Run this with: python lipi.py examples/error_message_demo.lipi.py --lang en
# Or: python lipi.py examples/error_message_demo.lipi.py --lang te

చెప్పు "Testing bilingual error messages..."
print "To see Telugu errors, run with: --lang te"

# Uncomment one test at a time to see different error messages:

# Test 1: Undefined variable error
# చెప్పు undefined_variable

# Test 2: Module not found error
# దిగుమతి something from "nonexistent_module"

# Test 3: Circular import (create two files that import each other to test)
# See test_circular.lipi.py

# Test 4: Invalid module path (path traversal)
# దిగుమతి hack from "../../../etc/passwd"

print "All tests passed! Uncomment tests above to see error messages."
చెప్పు "అన్ని పరీక్షలు విజయవంతం!"
