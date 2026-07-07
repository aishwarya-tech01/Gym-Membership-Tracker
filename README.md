# Gym Membership Subscription & Billing Tracker 🏋️‍♀️

A comprehensive, full-stack fitness center management application built with Python, Flask, and MySQL. This dashboard allows gym administrators to effortlessly track members, manage subscriptions, and monitor business revenue in real-time.

## 🌟 Key Features
* **Interactive Sidebar Registration:** Quickly onboard new gym members using a persistent sidebar form.
* **Smart Date Logic:** Automatically calculates membership expiration dates based on the selected tier (Monthly or Yearly) using Python's `datetime` logic.
* **Automated Expiration Flags:** Proactively identifies and highlights members whose subscriptions are expiring within the next 7 days using SQL interval queries.
* **Financial Aggregation:** Utilizes SQL `SUM` aggregations to instantly calculate and display the total generated monthly and yearly revenue.
* **Attendance Logger:** Efficiently track daily gym traffic and maintain a record of member visits.
* **CSV Export:** Generate and download reports of your member database for external record-keeping and analysis.

## 💻 Technologies Used
* **Backend:** Python 3, Flask Web Framework
* **Database:** MySQL, `mysql-connector-python`
* **Frontend:** HTML5, CSS3, Jinja2 Templating, Bootstrap
* **Environment Management:** Python Virtual Environment (`venv`)

## ⚙️ How to Run Locally

**1. Database Server**
Ensure your local MySQL server (XAMPP, WAMP, or MySQL Workbench) is actively running.

**2. Install Dependencies**
Open your terminal inside the project directory and install the necessary packages:
> `pip install flask mysql-connector-python`

**3. Initialize the Database**
Run the setup script to provision your database and tables automatically:
> `python setup_db.py`

**4. Launch the Application**
Start the backend web server:
> `python app.py`

**5. Access the Dashboard**
Open your web browser and navigate to:
`http://127.0.0.1:5000`
