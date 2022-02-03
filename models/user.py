from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from init import db

class User(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    username= db.Column(db.String(100000), nullable= False)
    password=db.Column(db.String(200), nullable= False)
    token=db.Column(db.String(200), default="no-token")
    def __repr__(self):
        return '<User id=%r username=%r>' % (self.id, self.username)


