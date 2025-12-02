# Test Calculator class with shorter string
print "Test: Calculator class"

class Calculator:
    function __init__(self, brand):
        self.brand = brand
        self.result = "0"
    end

    function add(self, a, b):
        self.result = a + b
        return self.result
    end

    function get_brand(self):
        return self.brand
    end
end

calc = Calculator("Test")
print "Brand: " + call calc.get_brand()
print "Done"
