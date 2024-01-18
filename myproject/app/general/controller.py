from . import general_bp
from flask import render_template, request
my_skills = ['Java', 'PHP', 'C++', 'MySQL','MPICH','OpenMP', 'JavaScript', 'Python', 'Spring Boot']
import os, datetime

menu = {
    'Homepage': 'general.home',
    'Posts': 'general.posts',
    'About': 'general.about',
    'Skills': 'general.skills',
    'Register': 'auth.register',
    'Login': 'auth.login',
    'Account': 'user.account',
    'Information': 'cookie.info',
    'Todo': 'todo.todo',
    'Feedback': 'feedback.feedback',
    'Logout': 'auth.logout'
}


@general_bp.route('/')
def home():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('home.html', data=data, menu=menu)

@general_bp.route('/posts')
def posts():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('posts.html', data=data, menu=menu)

@general_bp.route('/about')
def about():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    return render_template('about.html', data=data, menu=menu)

@general_bp.route("/skills", methods = ["GET"])
def skills():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    skill = request.args.get("skill", None)

    return render_template("skills.html", data=data, menu=menu, skills=my_skills, skill=skill, skills_len=len(my_skills))



