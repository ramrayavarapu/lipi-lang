# Test Calculator class
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

calc = Calculator("Lipi Calculator v3.0")
print "Brand: " + call calc.get_brand()
sum = call calc.add(10, 20)
print "10 + 20 = " + sum
print "Done"
