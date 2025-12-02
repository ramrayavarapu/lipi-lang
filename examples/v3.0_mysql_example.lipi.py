# v3.0 MySQL Database Example
# This example shows how to use MySQL database features in Lipi v3.0
#
# NOTE: This requires MySQL server running and mysql-connector-python installed:
# pip install mysql-connector-python
#
# To run this example, you need a MySQL server with:
# - Host: localhost
# - User: test_user
# - Password: test_password
# - Database: test_db

చెప్పు "=== Lipi v3.0 MySQL Example ==="
print ""

# Example 1: Connect to MySQL database (Telugu)
చెప్పు "Example 1: Connecting to MySQL (Telugu syntax)"
# db = mysql_కనెక్ట్("localhost", "test_user", "test_password", "test_db")
# చెప్పు "Connected to MySQL: " + db
print ""

# Example 2: Connect to MySQL database (English)
print "Example 2: Connecting to MySQL (English syntax)"
# db = mysql_connect("localhost", "test_user", "test_password", "test_db")
# print "Connected to MySQL: " + db
print ""

# Example 3: Create table
print "Example 3: Creating a table"
# mysql_query(db, "CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100), age INT)")
# print "Table created successfully"
print ""

# Example 4: Insert data with parameterized query (prevents SQL injection)
print "Example 4: Inserting data with parameters"
# affected = mysql_ప్రశ్న(db, "INSERT INTO users (name, age) VALUES (%s, %s)", ["రాము", 25])
# చెప్పు "Rows affected: " + affected
#
# affected2 = mysql_query(db, "INSERT INTO users (name, age) VALUES (%s, %s)", ["Sita", 23])
# print "Rows affected: " + affected2
print ""

# Example 5: Select data
print "Example 5: Querying data"
# users = mysql_query(db, "SELECT * FROM users")
# పునరావృతం user in users:
#     చెప్పు "User: " + user["name"] + " (Age: " + user["age"] + ")"
# ముగింపు
print ""

# Example 6: Update data
print "Example 6: Updating data"
# affected = mysql_query(db, "UPDATE users SET age = %s WHERE name = %s", [26, "రాము"])
# print "Rows updated: " + affected
print ""

# Example 7: Delete data
print "Example 7: Deleting data"
# affected = mysql_query(db, "DELETE FROM users WHERE age < %s", [20])
# print "Rows deleted: " + affected
print ""

# Example 8: Close connection
print "Example 8: Closing connection"
# result = mysql_close(db)
# print "Connection closed: " + result
print ""

చెప్పు "=== Complete MySQL Example ==="
print ""
print "Full working example (uncomment to run with real MySQL):"
print ""
print "# Connect"
print "db = mysql_connect(\"localhost\", \"user\", \"password\", \"database\")"
print ""
print "# Create table"
print "mysql_query(db, \"CREATE TABLE items (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(100))\")"
print ""
print "# Insert with parameters (SQL injection safe)"
print "mysql_query(db, \"INSERT INTO items (name) VALUES (%s)\", [\"Item 1\"])"
print ""
print "# Select data"
print "items = mysql_query(db, \"SELECT * FROM items\")"
print "for item in items:"
print "    print item[\"name\"]"
print "end"
print ""
print "# Close"
print "mysql_close(db)"
print ""

చెప్పు "=== MySQL Features Summary ==="
print "✅ mysql_connect() / mysql_కనెక్ట్() - Connect to MySQL"
print "✅ mysql_query() / mysql_ప్రశ్న() - Execute queries (SELECT, INSERT, UPDATE, DELETE)"
print "✅ mysql_close() / mysql_మూసివేయి() - Close connection"
print "✅ Parameterized queries - Prevents SQL injection"
print "✅ Dictionary results - Easy to access by column name"
print "✅ Bilingual support - Telugu and English keywords"
