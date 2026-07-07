from flask import Flask, render_template, request, redirect, url_for, Response
import mysql.connector
import datetime
import csv
import io

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
    
    # Search Filter Processing
    search_query = request.args.get('search', '')
    if search_query:
        sql = "SELECT * FROM members WHERE name LIKE %s OR phone LIKE %s"
        cursor.execute(sql, (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()
    
    # Dashboard Metrics Computations
    cursor.execute("SELECT COUNT(*) as total FROM members")
    total_members = cursor.fetchone()['total'] or 0
    
    cursor.execute("SELECT SUM(amount_paid) as total_revenue FROM members")
    total_revenue = cursor.fetchone()['total_revenue'] or 0
    
    today = datetime.date.today()
    cursor.execute("SELECT COUNT(*) as active FROM members WHERE expiry_date >= %s", (today,))
    active_members = cursor.fetchone()['active'] or 0
    
    # Fetch Today's Attendance Logs (Option 2)
    cursor.execute("""
        SELECT a.check_in_time, m.name 
        FROM attendance a 
        JOIN members m ON a.member_id = m.id 
        WHERE DATE(a.check_in_time) = %s 
        ORDER BY a.check_in_time DESC
    """, (today,))
    attendance_logs = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return render_template(
        'index.html', 
        members=members, 
        search_query=search_query,
        total_members=total_members,
        total_revenue=total_revenue,
        active_members=active_members,
        attendance_logs=attendance_logs,
        today=today
    )

@app.route('/add', methods=['POST'])
def add_member():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO members (name, phone, membership_type, amount_paid, join_date, expiry_date) 
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (request.form['name'], request.form['phone'], request.form['membership_type'], 
         request.form['amount_paid'], request.form['join_date'], request.form['expiry_date'])
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# FEATURE OPTION 1: Profile Modifications (Edit/Update Framework)
@app.route('/edit/<int:member_id>', methods=['GET', 'POST'])
def edit_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if request.method == 'POST':
        cursor.execute("""
            UPDATE members 
            SET name=%s, phone=%s, membership_type=%s, amount_paid=%s, join_date=%s, expiry_date=%s 
            WHERE id=%s
        """, (request.form['name'], request.form['phone'], request.form['membership_type'], 
              request.form['amount_paid'], request.form['join_date'], request.form['expiry_date'], member_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))
    
    cursor.execute("SELECT * FROM members WHERE id = %s", (member_id,))
    member = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit.html', member=member)

@app.route('/delete/<int:member_id>', methods=['GET'])
def delete_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM members WHERE id = %s", (member_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# FEATURE OPTION 2: Real-time Attendance Check-In Log entries
@app.route('/checkin/<int:member_id>', methods=['POST'])
def checkin_member(member_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO attendance (member_id, check_in_time) VALUES (%s, %s)",
        (member_id, datetime.datetime.now())
    )
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('index'))

# FEATURE OPTION 3: Export Entire Database To Spreadsheet (CSV Report)
@app.route('/export', methods=['GET'])
def export_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, phone, membership_type, amount_paid, join_date, expiry_date FROM members")
    rows = cursor.fetchall()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Phone', 'Plan Type', 'Amount Paid (₹)', 'Join Date', 'Expiry Date'])
    writer.writerows(rows)
    output.seek(0)
    
    cursor.close()
    conn.close()
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=gym_members_report.csv"}
    )

if __name__ == '__main__':
    app.run(debug=True)