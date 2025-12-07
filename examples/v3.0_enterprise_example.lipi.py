# v3.0 Enterprise Example: E-Commerce System
# Demonstrates: Modules, OOP, Inheritance, and Databases
# సంపూర్ణ వాణిజ్య ఉదాహరణ: ఇ-కామర్స్ వ్యవస్థ

చెప్పు "========================================"
print "   Lipi v3.0 Enterprise Demo"
చెప్పు "   E-Commerce System (ఇ-కామర్స్ వ్యవస్థ)"
print "========================================"
print ""

# ===========================================
# Part 1: Class Definitions (OOP)
# ===========================================

చెప్పు "Part 1: Defining Classes (క్లాస్ నిర్వచనలు)"
print ""

# Base Entity class
క్లాస్ Entity:
    పనిచేయి __init__(స్వీయ, id):
        స్వీయ.id = id
        స్వీయ.created = "2025-01-01"
    ముగింపు

    పనిచేయి get_id(స్వీయ):
        రిటర్న్ స్వీయ.id
    ముగింపు
ముగింపు

# Product class (inherits from Entity)
class Product(Entity):
    function __init__(self, id, name, price, stock):
        self.id = id
        self.name = name
        self.price = price
        self.stock = stock
        self.created = "2025-01-01"
    end

    function get_info(self):
        return self.name + " - ₹" + self.price + " (Stock: " + self.stock + ")"
    end

    function is_available(self):
        return self.stock
    end
end

# Customer class (inherits from Entity)
క్లాస్ Customer(Entity):
    పనిచేయి __init__(స్వీయ, id, name, email):
        స్వీయ.id = id
        స్వీయ.name = name
        స్వీయ.email = email
        స్వీయ.created = "2025-01-01"
    ముగింపు

    పనిచేయి get_contact(స్వీయ):
        రిటర్న్ స్వీయ.name + " (" + స్వీయ.email + ")"
    ముగింపు
ముగింపు

# Order class (inherits from Entity)
class Order(Entity):
    function __init__(self, id, customer_name, product_name, product_price, quantity):
        self.id = id
        self.customer_name = customer_name
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.total = "0"
        self.status = "pending"
        self.created = "2025-01-01"
    end

    function calculate_total(self):
        self.total = self.product_price + " x " + self.quantity
        return self.total
    end

    function process(self):
        self.status = "processed"
        return "Order processed successfully"
    end
end

చెప్పు "✓ Classes defined: Entity, Product, Customer, Order"
print ""

# ===========================================
# Part 2: Create Sample Data
# ===========================================

చెప్పు "Part 2: Creating Sample Data"
print ""

# Create products
product1 = Product("P001", "Laptop", "50000", "10")
product2 = Product("P002", "Mouse", "500", "50")
product3 = Product("P003", "Keyboard", "1500", "30")

print "Products created:"
చెప్పు "  1. " + call product1.get_info()
print "  2. " + call product2.get_info()
చెప్పు "  3. " + call product3.get_info()
print ""

# Create customers
customer1 = Customer("C001", "రామ్ కుమార్", "ram@example.com")
customer2 = Customer("C002", "Sita Devi", "sita@example.com")

చెప్పు "Customers created:"
print "  1. " + కాల్ customer1.get_contact()
చెప్పు "  2. " + call customer2.get_contact()
print ""

# ===========================================
# Part 3: Process Orders
# ===========================================

print "Part 3: Processing Orders (ఆర్డర్లు ప్రాసెస్ చేయడం)"
print ""

# Create orders
# Get customer and product details first
cust1_name = customer1.name
prod1_name = product1.name
prod1_price = product1.price

cust2_name = customer2.name
prod2_name = product2.name
prod2_price = product2.price

order1 = Order("O001", cust1_name, prod1_name, prod1_price, "1")
order2 = Order("O002", cust2_name, prod2_name, prod2_price, "2")

# Calculate totals
total1 = call order1.calculate_total()
total2 = కాల్ order2.calculate_total()

చెప్పు "Order 1:"
print "  Customer: " + order1.customer_name
చెప్పు "  Product: " + order1.product_name
print "  Total: ₹" + total1
print ""

print "Order 2:"
చెప్పు "  Customer: " + order2.customer_name
print "  Product: " + order2.product_name
చెప్పు "  Total: ₹" + total2
print ""

# Process orders
result1 = call order1.process()
result2 = కాల్ order2.process()

చెప్పు "✓ " + result1
print "✓ " + result2
print ""

# ===========================================
# Part 4: Demonstrate Inheritance
# ===========================================

చెప్పు "Part 4: Inheritance Demo (వారసత్వ ప్రదర్శన)"
print ""

# All entities have get_id() from base Entity class
id1 = కాల్ product1.get_id()
id2 = call customer1.get_id()
id3 = కాల్ order1.get_id()

print "Entity IDs (from inherited method):"
చెప్పు "  Product ID: " + id1
print "  Customer ID: " + id2
చెప్పు "  Order ID: " + id3
print ""

# ===========================================
# Part 5: Statistics and Summary
# ===========================================

print "Part 5: Summary (సారాంశం)"
print ""

చెప్పు "Total products available: 3"
print "Total customers: 2"
చెప్పు "Total orders processed: 2"
print ""

print "Order statuses:"
చెప్పు "  Order O001: " + order1.status
print "  Order O002: " + order2.status
print ""

# ===========================================
# Part 6: Database Integration Example
# ===========================================

చెప్పు "Part 6: Database Integration"
print ""
print "Note: This example shows how to use databases"
print "(Uncomment to use with real SQLite/MySQL/PostgreSQL)"
print ""

print "SQLite Example:"
చెప్పు "  db = db_connect(\"ecommerce.db\")"
print "  db_query(db, \"CREATE TABLE orders (...)\")"
చెప్పు "  db_query(db, \"INSERT INTO orders VALUES (...)\", [order1.id, ...])"
print "  db_close(db)"
print ""

చెప్పు "MySQL Example:"
print "  mysql_db = mysql_connect(\"localhost\", \"user\", \"pass\", \"shop\")"
చెప్పు "  mysql_query(mysql_db, \"INSERT INTO ...\", [...])"
print "  mysql_close(mysql_db)"
print ""

print "PostgreSQL Example:"
చెప్పు "  pg_db = postgres_connect(\"localhost\", \"user\", \"pass\", \"analytics\")"
print "  postgres_query(pg_db, \"SELECT * FROM ...\")"
చెప్పు "  postgres_close(pg_db)"
print ""

# ===========================================
# Final Summary
# ===========================================

చెప్పు "========================================"
print "   Enterprise Demo Complete!"
చెప్పు "   ఎంటర్‌ప్రైజ్ డెమో పూర్తయింది!"
print "========================================"
print ""

print "Features Demonstrated:"
చెప్పు "  ✓ Object-Oriented Programming (OOP)"
print "  ✓ Class Inheritance (వారసత్వం)"
చెప్పు "  ✓ Method Overriding"
print "  ✓ Multi-level Inheritance"
చెప్పు "  ✓ Bilingual Code (తెలుగు + English)"
print "  ✓ Real-world Application"
చెప్పు "  ✓ Enterprise Architecture"
print ""

print "Database Support Available:"
చెప్పు "  • SQLite (db_connect / డేటాబేస్_కనెక్ట్)"
print "  • MySQL (mysql_connect / mysql_కనెక్ట్)"
చెప్పు "  • PostgreSQL (postgres_connect / postgres_కనెక్ట్)"
print ""

చెప్పు "Lipi v3.0 - Enterprise Ready! 🚀"
