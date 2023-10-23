import datetime
import os
from flask import render_template, request, redirect, url_for, make_response, session
from app import app
import json


with open('users.json') as f:
    users = json.load(f)
my_skills = ['Java', 'PHP', 'C++', 'MySQL','MPICH','OpenMP', 'JavaScript', 'Python', 'Spring Boot']


@app.route('/')
def home():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('home.html', data=data)

@app.route('/posts')
def posts():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('posts.html', data=data)

@app.route('/about')
def about():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('about.html', data=data)

@app.route("/skills", methods = ["GET"])
def skills():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    skill = request.args.get("skill", None)

    return render_template("skills.html", data=data, skills=my_skills, skill=skill, skills_len=len(my_skills))
#http://127.0.0.1:5000/query?name=admin&password=1234


@app.route('/query', methods=["GET", "POST"])
def form():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if request.method == "POST":
        name = request.form.get("name")
        password = request.form.get("password")
        if name == "admin" and password == "1234":
            return redirect(url_for("home"))
    return render_template("my_form.html", data=data)

#http://127.0.0.1:5000/setcookie?userId=101
@app.route('/setcookie', methods=["GET"])
def cookie():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if request.args.get("userId"):
        user_value = request.args.get("userId") #101
        session["userId"] = user_value
        resp = make_response(f"Hi, set cookie {user_value}")
        resp.set_cookie("userId", user_value)
        return resp
    print(session.get("userId"))
    userId = request.cookies.get("userId")
    if not userId:
        userId = session.get("userId")

    return render_template("read_cookie.html", userID=userId)

@app.route('/clearcookie', methods=["GET"])
def clear_cookie():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    resp = make_response(f"Hi, delete  ")
    # resp.set_cookie("userId", "", expires=0)
    resp.delete_cookie("userId")
    return resp

@app.route('/clearsession', methods=["GET"])
def clear_session():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    session.pop("userId")
    return redirect(url_for("home"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(f"DEEEEEEE {username} {password}")
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('info'))
    return render_template('login.html', data=data)

@app.route('/info')
def info():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if 'username' in session:
        return render_template('info.html', username=session["username"], data=data)
    return redirect(url_for('login'), data=data)