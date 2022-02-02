from distutils.log import error
from email.policy import default
import math
from sqlalchemy.dialects.postgresql import UUID
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models.blogs import Blog
import uuid

app= Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///models/test.db'
db= SQLAlchemy(app)



@app.route('/')
def index():
    blogs=Blog.query.order_by(Blog.date_created).all()
    for blog in blogs:
        blog.date_created= blog.date_created.strftime("%d %B, %Y")
    # print(blogs)
    return render_template('index.html', blogs=blogs)

@app.route('/admin')
def admin():
    blogs=Blog.query.order_by(Blog.date_created).all()
    return render_template('admin.html', blogs=blogs)



@app.route('/admin/create', methods=['GET', 'POST'])
def create():
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


