from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    tags = db.relationship('Tag')

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    color = db.Column(db.String(50))
    tags = db.Column(db.Integer)
    harvest_date = db.Column(db.Date)
    average_weight = db.Column(db.Integer)
    price = db.Column(db.Float)
    total_sales = db.Column(db.Integer)
    note_id = db.Column(db.Integer, db.ForeignKey('note.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
