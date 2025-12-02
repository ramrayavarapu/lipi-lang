# Test with spaces in string argument
print "Testing class with spaced string"

class Box:
    function __init__(self, label):
        self.label = label
    end

    function show(self):
        print "Label: " + self.label
    end
end

box1 = Box("My Test Box")
call box1.show()
print "Success"
