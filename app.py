from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime, timedelta

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="", 
        database="gym_billing_db"
    )

@app.route("/")
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM Members ORDER BY expiry_date ASC")
    members = cursor.fetchall()
    
    cursor.execute("SELECT SUM(price) as total_revenue FROM Members")
    revenue_result = cursor.fetchone()
    total_revenue = revenue_result['total_revenue'] if revenue_result['total_revenue'] else 0

    cursor.close()
    conn.close()
    
    return render_template("index.html", members=members, total_revenue=total_revenue)

@app.route("/add", methods=["POST"])
def add_member():
    full_name = request.form.get("full_name")
    plan_type = request.form.get("plan_type")
    
    join_date = datetime.now().date()
    price = 50.00 if plan_type == 'Monthly' else 500.00
    expiry_date = join_date + (timedelta(days=30) if plan_type == 'Monthly' else timedelta(days=365))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Members (full_name, plan_type, price, join_date, expiry_date) VALUES (%s, %s, %s, %s, %s)", 
                   (full_name, plan_type, price, join_date, expiry_date))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)