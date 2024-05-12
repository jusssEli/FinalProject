from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from flask_session import Session
from models import db, User
import re

app = Flask(__name__)

app.config['SESSION_TYPE'] = 'sqlalchemy'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/keenconnect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'WXYZ9876'
app.config['SESSION_SQLALCHEMY'] = db

db.init_app(app)
Session(app)

@app.route("/")
def index():
    return redirect(url_for('dashboard'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:  # Check the hashed password here instead
            session['loggedin'] = True
            session['userid'] = user.user_id
            session['username'] = user.username
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Invalid credentials")
    else:
        return render_template("login.html", error=None)
    
@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        # If user is logged in, display dashboard
        return render_template("dashboard.html")
    else:
        # If not logged in, redirect to login page
        return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # Hash this password
        email = request.form['email']
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return render_template('register.html', message='Account already exists!')
        else:
            new_user = User(username=username, email=email, password=password)  # Hash the password before saving
            db.session.add(new_user)
            db.session.commit()
            session['loggedin'] = True
            session['username'] = username
            session['email'] = email
            return redirect(url_for('dashboard'))
    else:
        return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)