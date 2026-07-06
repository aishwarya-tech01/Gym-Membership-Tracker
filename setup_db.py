import mysql.connector

# Connect to XAMPP MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()

# Create the database if it doesn't exist
cursor.execute("CREATE DATABASE IF NOT EXISTS gym_billing_db")
cursor.execute("USE gym_billing_db")

# Drop the old table to upgrade to the new feature columns cleanly
cursor.execute("DROP TABLE IF EXISTS members")

# Create the updated table structure
cursor.execute("""
    CREATE TABLE members (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(15) NOT NULL,
        membership_type VARCHAR(50) NOT NULL,
        amount_paid INT NOT NULL,
        join_date DATE NOT NULL,
        expiry_date DATE NOT NULL
    )
""")

print("SUCCESS: New upgraded database schema built flawlessly!")

cursor.close()
conn.close()