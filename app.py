from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gym_billing_db"
    )

@app.route('/', methods=['GET'])
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    search_query = request.args.get('search', '')
    if search_query:
        sql = "SELECT * FROM members WHERE name LIKE %s OR phone LIKE %s"
        cursor.execute(sql, (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM members")
        
    members = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('index.html', members=members, search_query=search_query)

@app.route('/add', methods=['POST'])
def add_member():
    name = request.form['name']
    phone = request.form['phone']
    membership_type = request.form['membership_type']
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO members (name, phone, membership_type) VALUES (%s, %s, %s)",
        (name, phone, membership_type)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:member_id>', methods=['GET'])
def delete_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id = %s", (member_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)