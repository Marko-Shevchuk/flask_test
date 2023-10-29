import datetime
import os
from flask import render_template, request, redirect, url_for, make_response, session
from app import app
import json
from app.forms import LoginForm # .forms

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



@app.route('/logout', methods=["GET"])
def logout():
    session.pop("username")
    return redirect(url_for("login"))



@app.route('/login', methods=['GET', 'POST'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('info'))
    return render_template('login.html', data=data)

@app.route('/info', methods=['GET', 'POST'])
def info():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    message=""
    cookies = {}
    if 'username' in session:
        if request.method == 'POST':
            key = request.form['key']
            value = request.form['value']
            expiration = request.form['expiration']  
            cookies = request.cookies if request.cookies else {"none": "none"}
            if 'change_password' in request.form and users[session['username']] == request.form['old_password']:
                new_password = request.form['new_password']
                users[session['username']] = new_password  
                with open('users.json', 'w') as f:
                    json.dump(users, f)  # save updated users
                message = "Password changed successfully."
            if request.form['action'] == 'add':
                message = "Cookie added successfully!"
                response = make_response(render_template('info.html', username=session['username'], cookies=cookies, data=data, message=message))
                response.set_cookie(key, value, expires=datetime.datetime.strptime(expiration, '%Y-%m-%d'))
                return response
            elif request.form['action'] == 'delete':
                if key == 'all':
                    for key in request.cookies:
                        response.set_cookie(key, '', expires=0)
                    message = "All cookies deleted successfully!"
                    response = make_response(render_template('info.html', username=session['username'], cookies=cookies, data=data, message=message))
                    return response
                else:
                    message = "Cookie deleted successfully!"
                    response = make_response(render_template('info.html', username=session['username'], cookies=cookies, data=data, message=message))
                    response.set_cookie(key, '', expires=0)
                    return response

        return render_template('info.html', username=session['username'], cookies=cookies, data=data)
    return redirect(url_for('login'), data=data)


