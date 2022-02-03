from crypt import methods
from distutils.log import error
from email import message
from email.policy import default
from http import cookies
import math
from multiprocessing.sharedctypes import Value
from sqlalchemy.dialects.postgresql import UUID
from flask import Flask, render_template, request, redirect, make_response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.blogs import Blog
from models.message import Message
from init import db, app
from models.user import User 
import uuid

class create_user():
    def create(username, password):
        new_user=User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        print("New User Created")

# create_user.create("tahsin_protik", "password1234")

def authenticate(token):
    if token:
        user=User.query.filter_by(token=token).first()
        if user:
            return []
        else:
            raise error 
        
    else:
        raise error

@app.route('/')
def index():
    blogs=Blog.query.order_by(Blog.date_created).all()
    for blog in blogs:
        blog.date_created= blog.date_created.strftime("%d %B, %Y")
    # print(blogs)
    return render_template('index.html', blogs=blogs)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        res=[]
        if user==None:
            return render_template('login.html')
        if user.password!=password:
            return render_template('login.html')
        x=str(uuid.uuid4())
        user.token=x
        db.session.commit()
        res=make_response(redirect('/admin'))
        res.set_cookie("token", value=x)
        return res
    else:
        return render_template('login.html')

@app.route('/admin')
def admin():
    token=request.cookies.get('token')
    print(token)
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')
    blogs=Blog.query.order_by(Blog.date_created).all()
    return render_template('admin.html', blogs=blogs)

@app.route('/admin/message')
def getMessage():
    token=request.cookies.get("token")
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')
    
    messages=Message.query.order_by(Message.date_created).all()
    for x in messages:
        x.message=x.message.split('\n')
    return render_template('message.html', messages=messages)

@app.route('/contact', methods=['GET', 'POST'])
def message():
    if request.method=='POST':
        message_sender=request.form['sender']
        message_message=request.form['message']
        messages=Message.query.order_by(Message.date_created).all()
        id=0
        for x in messages:
            id=max(x.id, id)
        
        id=id+1
        new_message= Message(id=id, sender=message_sender, message=message_message)
        try:
            db.session.add(new_message)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(e)
            return redirect('/')
        
    else:
        return render_template('contact.html')

@app.route('/admin/create', methods=['GET', 'POST'])
def create():
    token=request.cookies.get("token")
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')

    if request.method=='POST':
        print(request.form)
        blog_intro=request.form['intro']
        blog_title=request.form['title']
        blog_content=request.form['content']
        blog_cover=request.form['cover']
        blogs=Blog.query.order_by(Blog.date_created).all()
        id=0
        for x in blogs:
            id=max(x.id, id)
        
        id=id+1
        new_blog= Blog(id=id, title=blog_title, content=blog_content, intro=blog_intro, cover=blog_cover)
        try:
            db.session.add(new_blog)
            db.session.commit()
            return redirect('/admin')
        except Exception as e:
            print(e)
            return redirect('/admin')
        
    else:
        return render_template('admin-create.html')

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):

    token=request.cookies.get("token")
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')

    if request.method=='POST':
        blog= Blog.query.filter_by(id = id).first()
        blog.title=request.form['title']
        blog.cover=request.form['cover']
        blog.intro=request.form['intro']
        blog.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/admin')
        except Exception as e:
            print(e)
            return redirect('/admin')
        
    else:
        blog= Blog.query.filter_by(id = id).first()
        print(blog)
        return render_template('admin-edit.html', blog=blog)

@app.route('/admin/delete/<int:id>')
def delete(id):
    token=request.cookies.get("token")
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')

    Blog.query.filter_by(id = id).delete()
    db.session.commit()
    return redirect('/admin')

@app.route('/blog/<int:id>')
def blog(id):
    # print(id)
    blog= Blog.query.filter_by(id = id).first()
    blog.content=blog.content.split('\n')
    blog.date_created= blog.date_created.strftime("%d %B, %Y | %I:%M %p")
    # print(blog)
    return render_template('blog.html', blog=blog)

if __name__=="__main__":
    app.run(debug=True)


