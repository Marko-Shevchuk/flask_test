import os, datetime
from flask import request, session, redirect, make_response, url_for, flash, render_template
from flask_login import login_required, current_user
from .forms import ChangePasswordForm
from app import db
from . import cookie_bp
from app.general.controller import menu

@cookie_bp.route('/setcookie', methods=["GET"])
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

    return render_template("cookie/read_cookie.html", userID=userId, data=data, menu=menu)

@cookie_bp.route('/info', methods=['GET', 'POST'])
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
            response = make_response(render_template('cookie/info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
            response.set_cookie(key, value, expires=datetime.datetime.strptime(expiration, '%Y-%m-%d'))
            return response
        elif request.form['action'] == 'delete':
            if key == 'all':
                for key in request.cookies:
                    response.set_cookie(key, '', expires=0)
                message = "All cookies deleted successfully!"
                response = make_response(render_template('cookie/info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                return response
            else:
                message = "Cookie deleted successfully!"
                response = make_response(render_template('cookie/info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, message=message, change_password_form=change_password_form))
                response.set_cookie(key, '', expires=0)
                return response
    
    return render_template('cookie/info.html', username=session['user']['login'], cookies=cookies, data=data, menu=menu, change_password_form=change_password_form)
   
@cookie_bp.route('/change_password', methods=['POST'])
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
    return redirect(url_for('cookie.info'))