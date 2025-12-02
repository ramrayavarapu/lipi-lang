# Debug Calculator issue
print "Test 1: Single assignment in __init__"

class Calc1:
    function __init__(self, brand):
        self.brand = brand
    end

    function get_brand(self):
        return self.brand
    end
end

c1 = Calc1("Test")
print "Calc1 OK"
print ""

print "Test 2: Two assignments in __init__"

class Calc2:
    function __init__(self, brand):
        self.brand = brand
        self.result = "0"
    end

    function get_brand(self):
        return self.brand
    end
end

c2 = Calc2("Test")
print "Calc2 OK"
