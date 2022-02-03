from email import message
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from init import db

class Message(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    sender= db.Column(db.String(200))
    message= db.Column(db.String(100000), nullable= False)
    date_created= db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Message id=%r sender=%r message=%r>' % (self.id, self.sender, self.message)
