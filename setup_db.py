import mysql.connector

# Connect directly to XAMPP MySQL Server instance
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()

# Initialize clean database structure
cursor.execute("CREATE DATABASE IF NOT EXISTS gym_billing_db")
cursor.execute("USE gym_billing_db")

# Drop old version of table to ensure structure upgrades cleanly
cursor.execute("DROP TABLE IF EXISTS members")

# Create fresh layout with proper columns
cursor.execute("""
    CREATE TABLE members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        membership_type VARCHAR(50) NOT NULL
    )
""")

print("SUCCESS: Database 'gym_billing_db' and table 'members' built cleanly!")

cursor.close()
conn.close()