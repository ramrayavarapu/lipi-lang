# v3.0 OOP Classes Test
# Testing basic class definitions, instantiation, and method calls

చెప్పు "=== v3.0 OOP Classes Test ==="
print ""

# Test 1: Telugu class definition with Telugu keywords
చెప్పు "Test 1: Telugu Person class"
క్లాస్ Person:
    పనిచేయి __init__(స్వీయ, name, age):
        స్వీయ.name = name
        స్వీయ.age = age
    ముగింపు

    పనిచేయి greet(స్వీయ):
        చెప్పు "నమస్తే, నేను " + స్వీయ.name
        చెప్పు "నా వయస్సు: " + స్వీయ.age
    ముగింపు

    పనిచేయి get_info(స్వీయ):
        రిటర్న్ స్వీయ.name + " (" + స్వీయ.age + " years old)"
    ముగింపు
ముగింపు

# Create instance and call methods
person1 = Person("రాము", "25")
కాల్ person1.greet()
info = కాల్ person1.get_info()
చెప్పు "Info: " + info
print ""

# Test 2: English class definition
print "Test 2: English Calculator class"
class Calculator:
    function __init__(self, brand):
        self.brand = brand
        self.result = "0"
    end

    function add(self, a, b):
        self.result = a + b
        return self.result
    end

    function multiply(self, a, b):
        self.result = a * b
        return self.result
    end

    function get_brand(self):
        return self.brand
    end
end

# Create calculator instance
calc = Calculator("Lipi Calculator v3.0")
print "Brand: " + call calc.get_brand()
sum = call calc.add(10, 20)
print "10 + 20 = " + sum
product = call calc.multiply(5, 7)
print "5 * 7 = " + product
print ""

# Test 3: Mixed Telugu and English
చెప్పు "Test 3: Mixed language class"
క్లాస్ Counter:
    function __init__(self, start):
        self.count = start
    end

    పనిచేయి increment(స్వీయ):
        స్వీయ.count = స్వీయ.count + 1
        రిటర్న్ స్వీయ.count
    ముగింపు

    function get_count(self):
        return self.count
    end
ముగింపు

counter = Counter(100)
print "Initial count: " + call counter.get_count()
new_count = కాల్ counter.increment()
చెప్పు "After increment: " + new_count
new_count2 = కాల్ counter.increment()
print "After second increment: " + new_count2
print ""

# Test 4: Class with no __init__
print "Test 4: Simple class without constructor"
class Greeter:
    function hello(self):
        return "Hello from Lipi v3.0!"
    end

    function goodbye(self):
        return "Goodbye!"
    end
end

greeter = Greeter()
msg1 = call greeter.hello()
print msg1
msg2 = call greeter.goodbye()
print msg2
print ""

చెప్పు "=== All OOP tests completed! ==="
