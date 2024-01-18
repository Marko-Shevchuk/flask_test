import datetime
import os
from flask import render_template, request, redirect, url_for, make_response, session, flash
from app import app
import json
from app import *
from app.forms import LoginForm, ChangePasswordForm, AddTask, UpdateTask, AddFeedback, RegisterForm
from app.domain.Todo import Task, Status
from app.domain.Feedback import Satisfaction, Feedback
from app.domain.User import User
from flask_login import login_user, current_user, login_required, logout_user
with open('users.json') as f:
    users = json.load(f)
my_skills = ['Java', 'PHP', 'C++', 'MySQL','MPICH','OpenMP', 'JavaScript', 'Python', 'Spring Boot']
menu = {
    'Homepage': 'home',
    'Posts': 'posts',
    'About': 'about',
    'Skills': 'skills',
    'Register': 'register',
    'Login': 'login',
    'Account': 'account',
    'Information': 'info',
    'Todo': 'todo',
    'Feedback': 'feedback',
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

@app.route('/account', methods=["GET"])
@login_required
def account():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template("account.html", data=data, menu=menu)

@app.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


@app.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('info'))
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
    login_form = LoginForm()
    session['login_form_login_value'] = login_form.login.data
    if login_form.validate_on_submit():
        entered_login = login_form.login.data
        entered_password = login_form.password.data
        user = User.query.filter(User.username == entered_login).first()
        if not user or not user.verify_password(entered_password):
            flash("Invalid credentials.", category="danger")
            return redirect(url_for('login'))
        if login_form.remember.data:
            login_user(user, remember=True)
            session.pop('login_form_login_value')
            flash("You successfully logged in.", category="success")
            return redirect(url_for("info"))
        login_user(user, remember=False)
    session['login_form_login_errors'] = login_form.login.errors
    session['login_form_password_errors'] = login_form.password.errors
    return redirect(url_for('login'))

@app.route('/register', methods=['GET'])
def register():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    form = RegisterForm()
    return render_template('register.html', form=form, data=data, menu=menu)


@app.route('/register', methods=['POST'])
def register_handle():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    register_form = RegisterForm()
    if not register_form.validate_on_submit():
        return render_template('register.html', form=register_form, data=data, menu=menu)
    username = register_form.username.data
    first_name = register_form.first_name.data
    last_name = register_form.last_name.data
    email = register_form.email.data
    password = register_form.password.data
    user = User(username=username,first_name = first_name, last_name = last_name, email = email,user_password = password)

    db.session.add(user)
    db.session.commit()
    flash(f"Successfully created account {register_form.username.data}.", category='success')
    return redirect(url_for('login'))

@app.route('/info', methods=['GET', 'POST'])
@login_required
def info():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    message=""
    cookies = {}
    change_password_form = ChangePasswordForm()

    if 'form_cp_errors' in session:
        change_password_form.new_password.errors = session.pop('form_cp_errors')
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']
        expiration = request.form['expiration']  
        cookies = request.cookies if request.cookies else {"none": "none"}
        
        if request.form['action'] == 'add':
            message = "Cookie added successfully!"
            response = make_response(render_template('info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
            response.set_cookie(key, value, expires=datetime.datetime.strptime(expiration, '%Y-%m-%d'))
            return response
        elif request.form['action'] == 'delete':
            if key == 'all':
                for key in request.cookies:
                    response.set_cookie(key, '', expires=0)
                message = "All cookies deleted successfully!"
                response = make_response(render_template('info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                return response
            else:
                message = "Cookie deleted successfully!"
                response = make_response(render_template('info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                response.set_cookie(key, '', expires=0)
                return response
    
    return render_template('info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, change_password_form=change_password_form)
   

@app.route('/change_password', methods=['POST'])
@login_required
def change_password():
    change_password_form = ChangePasswordForm()
    if change_password_form.validate_on_submit():
        new_password = change_password_form.new_password.data
        old_password = change_password_form.old_password.data

        if current_user.verify_password(old_password):
            current_user.user_password = new_password
            db.session.commit()

            flash("Successfully changed password.", category="success")
            return redirect(url_for('info'))

        flash("Incorrect old password.", category="error")
        session['form_cp_errors'] = change_password_form.errors
    return redirect(url_for('info'))

@app.route('/todo', methods=['GET'])
def todo():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    task_list = db.session.query(Task).all()
    return render_template('todo.html', tasks=task_list, data=data, menu=menu)


@app.route('/todo/add', methods=['GET', 'POST'])
@login_required
def add_task():
    data = [os.name, datetime.datetime.now(), request.user_agent]

    add_task_form = AddTask()
    if request.method == 'GET':
        return render_template('add_task.html', form=add_task_form, data=data, menu=menu)
    if add_task_form.validate_on_submit():
        task_name = add_task_form.name.data
        description = add_task_form.description.data

        existing_task = Task.query.filter(Task.name == task_name).first()
        if existing_task is not None:
            flash("There is ALREADY a task with this name.", category="danger")
            return redirect(url_for('add_task'))

        task = Task(name=task_name, description=description)
        db.session.add(task)
        db.session.commit()
        flash(f"Successfully created task {task_name}", category='success')
        return redirect(url_for('todo'))
    return render_template('add_task.html', form=add_task_form, data=data, menu=menu)


@app.route('/todo/<int:id>', methods=['GET'])
@login_required
def get_task(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    
    if id is None:
        return redirect(url_for('todo'))

    task = db.get_or_404(Task, id)
    update_form = UpdateTask()
    update_form.status.default = task.status.value
    return render_template('update_task.html', task=task, form=update_form, data=data, menu=menu)


@app.route('/todo/<int:id>', methods=['POST'])
@login_required
def update_task(id=None):
    data = [os.name, datetime.datetime.now(), request.user_agent]
    
    if id is None:
        return redirect(url_for('todo'))

    task = db.get_or_404(Task, id)
    update_form = UpdateTask()
    if not update_form.validate_on_submit():
        return render_template('update_task.html', task=task, form=update_form, data=data, menu=menu)

    name = update_form.name.data
    description = update_form.description.data
    status = Status[update_form.status.data]

    existing_task = db.session.query(Task).filter(Task.name == name).first()
    if existing_task is not None and existing_task.id != task.id:
        flash("There is ALREADY a task with this name.", category="danger")
        return redirect(url_for('add_task'))

    task.name = name
    task.description = description
    task.status = status
    db.session.commit()
    flash("Successfully updated task", category='success')
    return redirect(url_for('todo'))


@app.route('/todo/<int:id>/delete')
@login_required
def delete_task(id=None):
    if id is None:
        return redirect(url_for('todo'))

    task = db.get_or_404(Task, id)
    db.session.delete(task)
    db.session.commit()
    flash(f"Successfully deleted task {task.name}", category='success')
    return redirect(url_for('todo'))

@app.route('/feedback', methods=['GET'])
def feedback():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = AddFeedback()
    feedbacks = Feedback.query.all()
    return render_template('feedback.html', form=form, feedbacks=feedbacks, data=data, menu=menu)


@app.route('/feedback', methods=['POST'])
def add_feedback():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = AddFeedback()
    if not form.validate_on_submit():
        return render_template('feedback.html', form=form, data=data, menu=menu)

    feedback = form.feedback.data
    satisfaction = Satisfaction[form.satisfaction.data]

    user = None if not current_user.is_authenticated else current_user.username
    entity = Feedback(feedback=feedback, satisfaction=satisfaction, user=user)
    db.session.add(entity)
    db.session.commit()
    flash(f"Successfully added feedback.", category="success")
    return redirect(url_for('feedback'))