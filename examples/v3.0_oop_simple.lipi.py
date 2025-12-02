# Simple OOP test
print "Testing simple class"

class Box:
    function __init__(self, label):
        self.label = label
    end

    function show(self):
        print "Box label: " + self.label
    end
end

print "Creating box..."
box1 = Box("TestBox")
print "Box created"
call box1.show()
print "Done"
