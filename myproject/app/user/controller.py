from flask import redirect, url_for, flash, session, request, render_template
from flask_login import current_user, login_required
import os, datetime
from app import db
from app.auth.controller import delete_file, upload_file

from app.general.controller import menu

from . import user_bp
from .forms import UpdateUserForm
@user_bp.route('/account', methods=["GET"])
@login_required
def account():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = UpdateUserForm()
    form.about_me.data = current_user.about_me
    return render_template("user/account.html", form=form, data=data, menu=menu)

@user_bp.route('/account', methods=['POST'])
@login_required
def update_account():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = UpdateUserForm()
    if not form.validate_on_submit():
        return render_template('user/account.html', form=form, data=data, menu=menu)

    current_user.username = form.username.data
    current_user.email = form.email.data
    current_user.first_name = form.first_name.data
    current_user.last_name = form.last_name.data
    current_user.about_me = form.about_me.data

    if form.user_image.data:
        delete_file(current_user.image_file_name)
        current_user.image_file_name = upload_file(form.user_image.data)

    db.session.commit()

    flash('You successfully updated your account details!', category='success')
    return redirect(url_for('user.account'))
