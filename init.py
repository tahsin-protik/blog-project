from email.policy import default
from flask import Flask
from dotenv import load_dotenv
import os
load_dotenv()
app= Flask(__name__)

from pymongo import MongoClient
mongo_username=os.getenv('MONGO_USER')
mongo_password=os.getenv('MONGO_PASSWORD')
print(mongo_password)
connection_string= "mongodb+srv://"+mongo_username+":"+mongo_password+"@blog-project.pjhgo.mongodb.net/blogdb?retryWrites=true&w=majority"
client = MongoClient(connection_string)
mdb = client.blogdb