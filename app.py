from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, User, Room, Booking
from datetime import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = 'WXYZ9876'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/keenconnect'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route("/")
def index():
    return redirect(url_for('login'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['loggedin'] = True
            session['userid'] = user.user_id
            session['username'] = user.username
            session['email'] = user.email
            return redirect(url_for('dashboard'))
        else:
            return render_template("login.html", error="Invalid credentials")
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'loggedin' in session:
        return render_template("dashboard.html", username=session['username'])
    return redirect(url_for("login"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        if User.query.filter_by(email=email).first():
            return render_template('register.html', message='Account already exists!')
        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/book_room/<int:room_id>', methods=['GET', 'POST'])
def book_room(room_id):
    room = Room.query.get(room_id)
    if request.method == 'POST':
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        date_of_booking = request.form['booking_date']
        time_of_arrival = datetime.strptime(request.form['time_of_arrival'], '%Y-%m-%d %H:%M')
        time_of_departure = datetime.strptime(request.form['time_of_departure'], '%Y-%m-%d %H:%M')
        
        new_booking = Booking(
            date_of_booking=date_of_booking,
            time_of_arrival=time_of_arrival,
            time_of_departure=time_of_departure,
            room_id=room_id,
            user_id=session['userid']
        )
        db.session.add(new_booking)
        db.session.commit()
        return redirect(url_for('dashboard'))
    if room:
        return render_template('book_room.html', room=room)
    return 'Room not found!', 404

if __name__ == "__main__":
    app.run(debug=True)


@app.route('/listing')
def listing():
    cursor = mysql.connection.cursor()
    # Execute a query to fetch data
    cursor.execute("SELECT * FROM employee")
    # Fetch all rows from the result set
    mysql.connection.commit()
    data = cursor.fetchall()
    cursor.close()
    print(data)
    #return f"Done!! Query Result is {data}"
    return render_template('listing.html', data=data)

@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/search', methods = ['POST', 'GET'])
def search():
    if request.method == 'GET':
        return "Fill out the Search Form"

    if request.method == 'POST':
        name = request.form['name']
        emp_id = request.form['emp_id']
        cursor = mysql.connection.cursor()
        if name:
            cursor.execute("SELECT * from employee where name = %s",[name])
        if emp_id:
            cursor.execute("SELECT * from employee where emp_id = %s",[emp_id])
        mysql.connection.commit()
        data = cursor.fetchall()
        cursor.close()
        print(data)
        #return f"Done!! Query Result is {data}"
        return render_template('results.html', data=data)

@app.route('/meetings')
def meetings():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM meeting")
    meeting_data = cursor.fetchall()
    cursor.close()
    return render_template('meetings.html', meetings=meeting_data)

@app.route('/remove_meeting/<int:meeting_id>', methods=['POST'])
def remove_meeting(meeting_id):
    if request.method == 'POST':
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM meeting WHERE meeting_id = %s", [meeting_id])
        mysql.connection.commit()
        cursor.close()
        return redirect(url_for('meetings'))
