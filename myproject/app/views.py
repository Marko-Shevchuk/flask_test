import datetime
import os
from flask import render_template, request, redirect, url_for, make_response, session, flash
from app import app
import json
from app.forms import LoginForm, ChangePasswordForm # .forms

with open('users.json') as f:
    users = json.load(f)
my_skills = ['Java', 'PHP', 'C++', 'MySQL','MPICH','OpenMP', 'JavaScript', 'Python', 'Spring Boot']
menu = {
    'Homepage': 'home',
    'Posts': 'posts',
    'About': 'about',
    'Skills': 'skills',
    'Login': 'login',
    'Information': 'info',
    'Logout': 'logout'
}



@app.route('/')
def home():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('home.html', data=data, menu=menu)

@app.route('/posts')
def posts():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('posts.html', data=data, menu=menu)

@app.route('/about')
def about():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('about.html', data=data, menu=menu)

@app.route("/skills", methods = ["GET"])
def skills():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    skill = request.args.get("skill", None)

    return render_template("skills.html", data=data, menu=menu, skills=my_skills, skill=skill, skills_len=len(my_skills))



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
    if 'username' in session:
        session.pop("username")
    return redirect(url_for("login"))


@app.route('/login', methods=['GET'])
def login():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    login_form = LoginForm()
    if 'login_form_login_errors' in session:
        login_form.login.errors = session.pop('login_form_login_errors')
    if 'login_form_password_errors' in session:
        login_form.password.errors = session.pop('login_form_password_errors')
    if 'login_form_login_value' in session:
        login_form.login.data = session.pop('login_form_login_value')
    return render_template('login.html', data=data, menu=menu, login_form=login_form)

@app.route('/login', methods=['POST'])
def login_handle():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    login_form = LoginForm()
    session['login_form_login_username'] = login_form.login.data
    if login_form.validate_on_submit():
        with open('users.json', 'r') as users:
            login_username = login_form.login.data
            password = login_form.password.data
            json_data = json.load(users)
            if json_data.get(login_username) is not None:
                user_data = json_data[login_username]
                if user_data['password'] == password:
                    del user_data['password'] 
                    if login_form.remember.data:
                        session['username'] = user_data
                        session['username']['login'] = login_username
                        session.pop('login_form_login_username')
                    flash("You successfully logged in.", category="success")
                    return redirect(url_for("info"))
            flash("Invalid credentials.", category="danger")
            return redirect(url_for('login'))
    session['login_form_login_errors'] = login_form.login.errors
    session['login_form_password_errors'] = login_form.password.errors
    return redirect(url_for('login'))


@app.route('/info', methods=['GET', 'POST'])
def info():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    message=""
    cookies = {}
    change_password_form = ChangePasswordForm()
    
    if 'username' in session:
        if 'form_cp_errors' in session:
            change_password_form.new_password.errors = session.pop('form_cp_errors')
        if request.method == 'POST':
            key = request.form['key']
            value = request.form['value']
            expiration = request.form['expiration']  
            cookies = request.cookies if request.cookies else {"none": "none"}
            
            if request.form['action'] == 'add':
                message = "Cookie added successfully!"
                response = make_response(render_template('info.html', username=session['username'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                response.set_cookie(key, value, expires=datetime.datetime.strptime(expiration, '%Y-%m-%d'))
                return response
            elif request.form['action'] == 'delete':
                if key == 'all':
                    for key in request.cookies:
                        response.set_cookie(key, '', expires=0)
                    message = "All cookies deleted successfully!"
                    response = make_response(render_template('info.html', username=session['username'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                    return response
                else:
                    message = "Cookie deleted successfully!"
                    response = make_response(render_template('info.html', username=session['username'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                    response.set_cookie(key, '', expires=0)
                    return response
        
        return render_template('info.html', username=session['username']['login'], cookies=cookies, data=data, menu=menu, change_password_form=change_password_form)
    return redirect(url_for('login'))

@app.route('/change_password', methods=['POST'])
def change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        user_login = session['user']['login']
        with open('users.json', 'r') as file:
            data = json.load(file)
        
        new_password = change_password_form.new_password.data
        if data[user_login]['password'] == change_password_form.old_password.data:
            data[user_login]['password'] = new_password
            with open('users.json', 'w') as file:
                json.dump(data, file)
            flash("You successfully changed your password!", category="success")

        
        return redirect(url_for('info'))
    session['form_cp_errors'] = change_password_form.new_password.errors
    return redirect(url_for('info'))
