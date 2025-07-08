from flask_login import UserMixin #https://youtu.be/dam0GPOAvVI?t=4993
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func #Könnten damit speichern, wann ein Spickzettel hochgeladen wurde

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    pw = db.Column(db.String, nullable=False)
    credits = db.Column(db.Integer, default=0, nullable=False)
    userart = db.Column(db.String, default="not verified", nullable=False)

#class Module(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String, nullable=False)

#class Professor(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String, nullable=False)
    #module_id = db.Column(db.Integer, db.ForeignKey('module.id'))

class Cheatsheet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    creditcost = db.Column(db.Integer, default=1, nullable=True)
    pdf_datei = db.Column(db.LargeBinary, nullable=False)
    module = db.Column(db.String, nullable=False)
    professor = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    votes = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=func.now())


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    creditamout = db.Column(db.Integer, nullable=False)

class UserCheatsheetAccess(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    cheatsheet_id = db.Column(db.Integer, db.ForeignKey('cheatsheet.id'), nullable=False, primary_key=True)
    vote = db.Column(db.Integer, default=0, nullable=False)

