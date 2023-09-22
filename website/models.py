#database schema 

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column (db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(88))
    username = db.Column(db.String(128), unique=True)
    notes = db.relationship('Note', backref='user', lazy='dynamic')
    darkmode = db.relationship('DarkMode', viewonly=True, back_populates="user")


class DarkMode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    darkModeEnabled = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    user = db.relationship('User', viewonly=True, back_populates="darkmode")


class DeletedNote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column (db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))








