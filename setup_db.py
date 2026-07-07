import mysql.connector

# Connect to XAMPP MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS gym_billing_db")
cursor.execute("USE gym_billing_db")

# Drop tables to clear out the old mismatched structure cleanly
cursor.execute("DROP TABLE IF EXISTS attendance")
cursor.execute("DROP TABLE IF EXISTS members")

# 1. Create Upgraded Members Table
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

# 2. Create Attendance Table
cursor.execute("""
    CREATE TABLE attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        member_id INT NOT NULL,
        check_in_time DATETIME NOT NULL,
        FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE CASCADE
    )
""")

print("SUCCESS: Advanced relational database tables built successfully!")

cursor.close()
conn.close()