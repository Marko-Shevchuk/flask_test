import datetime, os, uuid
from PIL import Image
from flask import current_app
from flask import session, redirect, url_for, flash, request, render_template
from flask_login import login_user, current_user, login_required, logout_user

from app import db
from app.domain.User import User
from . import auth_bp
from .forms import LoginForm, RegisterForm
from app.general.controller import menu
def upload_file(file):
    if not file:
        return

    filename, extension = file.filename.rsplit('.', 1)
    uuid_name = uuid.uuid4()
    secured_filename = f"{uuid_name}.{extension}"
    path = os.path.join(current_app.config["IMAGES_FOLDER"], secured_filename)

    image = Image.open(file)
    image.thumbnail((512, 512))
    image.save(path)
    return secured_filename

def delete_file(file_name):
    path = os.path.join(current_app.config["IMAGES_FOLDER"], file_name)
    if file_name != current_app.config["IMAGES_DEFAULT_NAME"] and os.path.exists(path):
        os.remove(path)

@auth_bp.route('/logout', methods=["GET"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth_bp.route('/login', methods=['GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('cookie.info'))
    data = [os.name, datetime.datetime.now(), request.user_agent]
    login_form = LoginForm()
    if 'login_form_login_errors' in session:
        login_form.login.errors = session.pop('login_form_login_errors')
    if 'login_form_password_errors' in session:
        login_form.password.errors = session.pop('login_form_password_errors')
    if 'login_form_login_value' in session:
        login_form.login.data = session.pop('login_form_login_value')
    return render_template('auth/login.html', data=data, menu=menu, login_form=login_form)

@auth_bp.route('/login', methods=['POST'])
def login_handle():
    login_form = LoginForm()
    session['login_form_login_value'] = login_form.login.data
    if login_form.validate_on_submit():
        entered_login = login_form.login.data
        entered_password = login_form.password.data
        user = User.query.filter(User.username == entered_login).first()
        if not user or not user.verify_password(entered_password):
            flash("Invalid credentials.", category="danger")
            return redirect(url_for('auth.login'))
        if login_form.remember.data:
            login_user(user, remember=True)
            session.pop('login_form_login_value')
            flash("You successfully logged in.", category="success")
            return redirect(url_for("cookie.info"))
        login_user(user, remember=False)
    session['login_form_login_errors'] = login_form.login.errors
    session['login_form_password_errors'] = login_form.password.errors
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET'])
def register():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    if current_user.is_authenticated:
        return redirect(url_for('info'))
    form = RegisterForm()
    return render_template('auth/register.html', form=form, data=data, menu=menu)


@auth_bp.route('/register', methods=['POST'])
def register_handle():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    register_form = RegisterForm()
    if not register_form.validate_on_submit():
        return render_template('auth/register.html', form=register_form, data=data, menu=menu)
    username = register_form.username.data
    first_name = register_form.first_name.data
    last_name = register_form.last_name.data
    email = register_form.email.data
    password = register_form.password.data
    image_file = register_form.user_image.data
    image_file_name = upload_file(image_file)
    user = User(username=username,first_name = first_name, last_name = last_name, email = email,user_password = password, image_file_name=image_file_name)

    db.session.add(user)
    db.session.commit()
    flash(f"Successfully created account {register_form.username.data}.", category='success')
    return redirect(url_for('auth.login'))

@auth_bp.after_request
def after_request(response):
    if current_user:
        current_user.last_seen = datetime.datetime.now()
        try:
            db.session.commit()
        except:
            flash(f"Error updating last seen time.", category='danger')
    return response