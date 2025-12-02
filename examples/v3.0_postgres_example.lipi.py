# v3.0 PostgreSQL Database Example
# This example shows how to use PostgreSQL database features in Lipi v3.0
#
# NOTE: This requires PostgreSQL server running and psycopg2 installed:
# pip install psycopg2-binary
#
# To run this example, you need a PostgreSQL server with:
# - Host: localhost
# - User: test_user
# - Password: test_password
# - Database: test_db
# - Port: 5432 (default)

చెప్పు "=== Lipi v3.0 PostgreSQL Example ==="
print ""

# Example 1: Connect to PostgreSQL database (Telugu)
చెప్పు "Example 1: Connecting to PostgreSQL (Telugu syntax)"
# db = postgres_కనెక్ట్("localhost", "test_user", "test_password", "test_db")
# చెప్పు "Connected to PostgreSQL: " + db
print ""

# Example 2: Connect to PostgreSQL database (English with custom port)
print "Example 2: Connecting to PostgreSQL (English syntax with custom port)"
# db = postgres_connect("localhost", "test_user", "test_password", "test_db", "5432")
# print "Connected to PostgreSQL: " + db
print ""

# Example 3: Create table
print "Example 3: Creating a table"
# postgres_query(db, "CREATE TABLE IF NOT EXISTS employees (id SERIAL PRIMARY KEY, name VARCHAR(100), salary INT)")
# print "Table created successfully"
print ""

# Example 4: Insert data with parameterized query (prevents SQL injection)
print "Example 4: Inserting data with parameters"
# affected = postgres_ప్రశ్న(db, "INSERT INTO employees (name, salary) VALUES (%s, %s)", ["రామ్", 50000])
# చెప్పు "Rows affected: " + affected
#
# affected2 = postgres_query(db, "INSERT INTO employees (name, salary) VALUES (%s, %s)", ["Sita", 60000])
# print "Rows affected: " + affected2
print ""

# Example 5: Select data
print "Example 5: Querying data"
# employees = postgres_query(db, "SELECT * FROM employees ORDER BY salary DESC")
# పునరావృతం emp in employees:
#     చెప్పు "Employee: " + emp["name"] + " - Salary: " + emp["salary"]
# ముగింపు
print ""

# Example 6: Update data
print "Example 6: Updating data"
# affected = postgres_query(db, "UPDATE employees SET salary = %s WHERE name = %s", [55000, "రామ్"])
# print "Rows updated: " + affected
print ""

# Example 7: Delete data
print "Example 7: Deleting data"
# affected = postgres_query(db, "DELETE FROM employees WHERE salary < %s", [30000])
# print "Rows deleted: " + affected
print ""

# Example 8: Using PostgreSQL-specific features
print "Example 8: PostgreSQL-specific features"
# Example: RETURNING clause (PostgreSQL feature)
# result = postgres_query(db, "INSERT INTO employees (name, salary) VALUES (%s, %s) RETURNING id", ["John", 70000])
# చెప్పు "New employee ID: " + result[0]["id"]
print ""

# Example 9: Close connection
print "Example 9: Closing connection"
# result = postgres_close(db)
# print "Connection closed: " + result
print ""

చెప్పు "=== Complete PostgreSQL Example ==="
print ""
print "Full working example (uncomment to run with real PostgreSQL):"
print ""
print "# Connect"
print "db = postgres_connect(\"localhost\", \"user\", \"password\", \"database\")"
print ""
print "# Create table"
print "postgres_query(db, \"CREATE TABLE products (id SERIAL PRIMARY KEY, name VARCHAR(100), price DECIMAL)\")"
print ""
print "# Insert with parameters (SQL injection safe)"
print "postgres_query(db, \"INSERT INTO products (name, price) VALUES (%s, %s)\", [\"Product 1\", 99.99])"
print ""
print "# Select data"
print "products = postgres_query(db, \"SELECT * FROM products\")"
print "for product in products:"
print "    print product[\"name\"] + \": $\" + product[\"price\"]"
print "end"
print ""
print "# Close"
print "postgres_close(db)"
print ""

చెప్పు "=== PostgreSQL Features Summary ==="
print "✅ postgres_connect() / postgres_కనెక్ట్() - Connect to PostgreSQL"
print "✅ postgres_query() / postgres_ప్రశ్న() - Execute queries (SELECT, INSERT, UPDATE, DELETE)"
print "✅ postgres_close() / postgres_మూసివేయి() - Close connection"
print "✅ Parameterized queries - Prevents SQL injection"
print "✅ Dictionary results - Easy to access by column name"
print "✅ PostgreSQL-specific features - RETURNING, SERIAL, etc."
print "✅ Custom port support - Default 5432 or specify your own"
print "✅ Bilingual support - Telugu and English keywords"
