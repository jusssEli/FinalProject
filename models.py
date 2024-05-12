from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)

class Room(db.Model):
    __tablename__ = 'room'
    room_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    image1 = db.Column(db.String(255))
    view = db.Column(db.String(80))
    width = db.Column(db.String(80))
    mx_capacity = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default="available")

class Booking(db.Model):
    __tablename__ = "booking"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_of_booking = db.Column(db.Date, nullable=False)
    time_of_arrival = db.Column(db.DateTime, nullable=False)
    time_of_departure = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default="pending")
    room_id = db.Column(db.Integer, db.ForeignKey('room.room_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    room = db.relationship('Room', backref='bookings', lazy='joined')
    user = db.relationship('User', backref='bookings', lazy='joined')