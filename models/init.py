from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db= SQLAlchemy(app)