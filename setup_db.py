import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="", 
        database="gym_billing_db"
    )

def setup_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Create Members table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            full_name VARCHAR(100),
            plan_type VARCHAR(50),
            price DECIMAL(10, 2),
            join_date DATE,
            expiry_date DATE
        )
    """)
    
    print("Database and table successfully created!")
    cursor.close()
    conn.close()

if __name__ == "__main__":
    setup_database()