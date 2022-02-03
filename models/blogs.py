from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
from init import db

class Blog(db.Model):
    id = db.Column(db.Integer,  primary_key=True)
    title= db.Column(db.String(200), nullable= False)
    content= db.Column(db.String(100000), nullable= False)
    intro=db.Column(db.String(200))
    date_created= db.Column(db.DateTime, default=datetime.utcnow)
    cover=db.Column(db.String(500))
    def __repr__(self):
        return '<Blog id=%r title=%r content=%r, intro=%r date_created= %r>' % (self.id, self.title, self.content, self.intro, self.date_created) 


