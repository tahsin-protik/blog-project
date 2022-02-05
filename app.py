from flask import Flask, render_template, request, redirect, make_response
from datetime import datetime
from init import app, mdb
import uuid
from collections import namedtuple
import json

class create_user():
    def create(username, password):
        new_user={"username": username, "password": password, "token": "no-token"}
        mdb.user.insert_one(new_user)

def getAllBlogs():
    blogs=list(mdb.blog.find({}))
    l=len(blogs)
    for i in range(0, l):
        del blogs[i]['_id']
        print(blogs[i]['date_created'])
        blogs[i]['date_created']= blogs[i]['date_created'].strftime("%d %B, %Y")
        blogs[i]= namedtuple("blog", blogs[i].keys())(*blogs[i].values())
    return blogs

def getSingleBlog(id, change=True):
    blog=mdb.blog.find_one({"id": id})
    del blog['_id']
    if change==True:
        blog['date_created']= blog['date_created'].strftime("%d %B, %Y")
        blog['content']=blog['content'].split('\n')
    blog= namedtuple("blog", blog.keys())(*blog.values())
    return blog

def getAllMessages():
    messages=list(mdb.message.find({}))
    print(messages)
    l=len(messages)
    for i in range(0, l):
        del messages[i]['_id']
        messages[i]['message']=messages[i]['message'].split('\n')
        messages[i]= namedtuple("message", messages[i].keys())(*messages[i].values())
    return messages


def authenticate(token):
    if token:
        user=mdb.user.find_one({"token": token})
        if user:
            return []
        else:
            raise error 
        
    else:
        raise error

@app.route('/')
def index():
    blogs=getAllBlogs()
    return render_template('index.html', blogs=blogs)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=mdb.user.find_one({"username": username})
        res=[]
        if user==None:
            return render_template('login.html')
        if user['password']!=password:
            return render_template('login.html')
        x=str(uuid.uuid4())
        mdb.user.update_one({'username': username}, {'$set': {'token': x} })
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
    blogs=getAllBlogs()
    return render_template('admin.html', blogs=blogs)

@app.route('/admin/message')
def getMessage():
    token=request.cookies.get("token")
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')
    
    messages=getAllMessages()
    return render_template('message.html', messages=messages)

@app.route('/contact', methods=['GET', 'POST'])
def message():
    if request.method=='POST':
        message_sender=request.form['sender']
        message_message=request.form['message']
        messages=getAllMessages()
        id=0
        for x in messages:
            id=max(x.id, id)
        
        id=id+1
        new_message= {"id": id, "sender": message_sender, "message": message_message}
        try:
            mdb.message.insert_one(new_message)
            return redirect('/')
        except Exception as e:
            print(e)
            return redirect('/')
        
    else:
        return render_template('contact.html')

@app.route('/admin/create', methods=['GET', 'POST'])
def create():
    # token=request.cookies.get("token")
    # try:
    #     authenticate(token)
    # except:
    #     return redirect('/admin/login')

    if request.method=='POST':
        print(request.form)
        blog_intro=request.form['intro']
        blog_title=request.form['title']
        blog_content=request.form['content']
        blog_cover=request.form['cover']
        blog_date_created=datetime.utcnow()
        blog=mdb.blog
        # blogs=json.loads(blog.find())
        # id=0
        # for x in blogs:
        #     id=max(x["id"], id)
        id=1
        new_blog= {"intro": blog_intro, "title": blog_title, "content": blog_content, "cover":blog_cover, "id": id, "date_created": blog_date_created}
        
        try:
            blog.insert_one(new_blog)
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
        blog_title=request.form['title']
        blog_cover=request.form['cover']
        blog_intro=request.form['intro']
        blog_content=request.form['content']

        edited_blog= {"intro": blog_intro, "title": blog_title, "content": blog_content, "cover":blog_cover}

        try:
            mdb.blog.update_one({'id': id}, {'$set' : edited_blog})
            return redirect('/admin')
        except Exception as e:
            print(e)
            return redirect('/admin')
        
    else:
        blog= getSingleBlog(id, False)
        return render_template('admin-edit.html', blog=blog)

@app.route('/admin/delete/<int:id>')
def delete(id):
    token=request.cookies.get("token")
    try:
        authenticate(token)
    except:
        return redirect('/admin/login')
    mdb.blog.delete_one({'id': id})
    return redirect('/admin')

@app.route('/blog/<int:id>')
def blog(id):
    # print(id)
    blog= getSingleBlog(id)
    
    # print(blog)
    return render_template('blog.html', blog=blog)

if __name__=="__main__":
    app.run(debug=True)


