import datetime
import os
from flask import render_template, request, redirect, url_for, make_response, session
from app import app
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

