from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'keenConnect'
app.config['DEBUG'] = True
  
mysql = MySQL(app)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Query the users table to check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        users = cursor.fetchone()
        if users:
            # If user exists and credentials are correct, create a session ID and redirect to user profile
            session['loggedin'] = True
            session['userid'] = users['userid']
            session['name'] = users['name']
            session['email'] = users['email']
            return render_template('user.html', error=None)
        else:
            # If credentials are incorrect, show login page again with an error message
            return render_template("login.html", error="Invalid credentials")
    else:
        # Display login page
        return render_template("login.html", error=None)
    
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))
  
@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form :
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not userName or not password or not email:
            message = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO users VALUES (NULL, % s, % s, % s)', (userName, email, password, ))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message = message)

@app.route("/dashboard")
def dashboard():
    session_id = request.cookies.get("session_id")
    if session_id:
        # Check if the session ID is valid and display dashboard if logged in
        # You can fetch user-specific data from the database and pass it to the dashboard template
        return render_template("dashboard.html")
    else:
        # If not logged in, redirect to the login page
        return redirect(url_for("login"))

if __name__ == "__main__":
    app.secret_key = '1z2y3x4wabc'
    app.run(debug=True)