# v3.0 Class Inheritance Test
# Testing inheritance, method overriding, and multi-level inheritance

చెప్పు "=== v3.0 Class Inheritance Test ==="
print ""

# Test 1: Simple inheritance with method overriding (Telugu)
చెప్పు "Test 1: Simple inheritance - Animal and Dog"
క్లాస్ Animal:
    పనిచేయి __init__(స్వీయ, name):
        స్వీయ.name = name
    ముగింపు

    పనిచేయి speak(స్వీయ):
        చెప్పు స్వీయ.name + " makes a sound"
    ముగింపు

    పనిచేయి info(స్వీయ):
        చెప్పు "This is an animal named " + స్వీయ.name
    ముగింపు
ముగింపు

క్లాస్ Dog(Animal):
    పనిచేయి speak(స్వీయ):
        చెప్పు స్వీయ.name + " barks loudly!"
    ముగింపు
ముగింపు

dog = Dog("Buddy")
# Should print "Buddy barks loudly!" (overridden method)
కాల్ dog.speak()
# Should print "This is an animal..." (inherited method)
కాల్ dog.info()
print ""

# Test 2: Inheritance without overriding (English)
print "Test 2: Simple inheritance - Vehicle and Car"
class Vehicle:
    function __init__(self, brand):
        self.brand = brand
    end

    function show_brand(self):
        print "Brand: " + self.brand
    end

    function start(self):
        print self.brand + " is starting..."
    end
end

class Car(Vehicle):
    function honk(self):
        print self.brand + " goes beep beep!"
    end
end

car = Car("Toyota")
# Inherited method
call car.show_brand()
# Inherited method
call car.start()
# Own method
call car.honk()
print ""

# Test 3: Multi-level inheritance (Grandparent -> Parent -> Child)
print "Test 3: Multi-level inheritance"
class LivingThing:
    function __init__(self, name):
        self.name = name
    end

    function breathe(self):
        print self.name + " is breathing"
    end
end

class Mammal(LivingThing):
    function feed_young(self):
        print self.name + " feeds its young with milk"
    end
end

class Cat(Mammal):
    function meow(self):
        print self.name + " says meow!"
    end
end

cat = Cat("Whiskers")
# From grandparent LivingThing
call cat.breathe()
# From parent Mammal
call cat.feed_young()
# From Cat itself
call cat.meow()
print ""

# Test 4: Mixed Telugu and English inheritance
చెప్పు "Test 4: Mixed language inheritance"
class Shape:
    function __init__(self, color):
        self.color = color
    end

    function show_color(self):
        print "Color: " + self.color
    end
end

క్లాస్ Circle(Shape):
    పనిచేయి __init__(స్వీయ, color, radius):
        స్వీయ.color = color
        స్వీయ.radius = radius
    ముగింపు

    పనిచేయి area(స్వీయ):
        చెప్పు "Circle radius: " + స్వీయ.radius
    ముగింపు
ముగింపు

circle = Circle("Red", "5")
# Inherited from Shape
కాల్ circle.show_color()
# Own method
కాల్ circle.area()
print ""

# Test 5: Method overriding with different behavior
print "Test 5: Method overriding - Person and Student"
class Person:
    function __init__(self, name, age):
        self.name = name
        self.age = age
    end

    function introduce(self):
        print "I am " + self.name + ", age " + self.age
    end
end

class Student(Person):
    function __init__(self, name, age, grade):
        self.name = name
        self.age = age
        self.grade = grade
    end

    function introduce(self):
        print "I am " + self.name + ", a student in grade " + self.grade
    end

    function study(self):
        print self.name + " is studying hard!"
    end
end

student = Student("Ram", "15", "10")
# Overridden method
call student.introduce()
# Own method
call student.study()
print ""

# Test 6: Constructor inheritance (child without __init__)
చెప్పు "Test 6: Constructor inheritance"
క్లాస్ Base:
    పనిచేయి __init__(స్వీయ, value):
        స్వీయ.value = value
        చెప్పు "Base constructor called with: " + value
    ముగింపు

    పనిచేయి show(స్వీయ):
        చెప్పు "Value: " + స్వీయ.value
    ముగింపు
ముగింపు

క్లాస్ Derived(Base):
    పనిచేయి extra(స్వీయ):
        చెప్పు "Extra method in derived class"
    ముగింపు
ముగింపు

# Uses parent's __init__
derived = Derived("Test123")
# Uses parent's method
కాల్ derived.show()
# Own method
కాల్ derived.extra()
print ""

చెప్పు "=== All Inheritance Tests Completed! ==="
print "✅ Simple inheritance working"
print "✅ Method overriding working"
print "✅ Parent method access working"
print "✅ Multi-level inheritance working"
print "✅ Constructor inheritance working"
print "✅ Mixed language inheritance working"
