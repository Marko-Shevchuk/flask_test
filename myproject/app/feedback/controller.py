from flask import redirect, url_for, flash, render_template, request
from flask_login import current_user
import os, datetime
from app import db
from app.general.controller import menu

from app.domain.Feedback import Satisfaction, Feedback
from . import feedback_bp
from .forms import AddFeedback

@feedback_bp.route('/feedback', methods=['GET'])
def feedback():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = AddFeedback()
    feedbacks = Feedback.query.all()
    return render_template('feedback/feedback.html', form=form, feedbacks=feedbacks, data=data, menu=menu)


@feedback_bp.route('/feedback', methods=['POST'])
def add_feedback():
    data = [os.name, datetime.datetime.now(), request.user_agent]
    form = AddFeedback()
    if not form.validate_on_submit():
        return render_template('feedback/feedback.html', form=form, data=data, menu=menu)

    feedback = form.feedback.data
    satisfaction = Satisfaction[form.satisfaction.data]

    user = None if not current_user.is_authenticated else current_user.username
    entity = Feedback(feedback=feedback, satisfaction=satisfaction, user=user)
    db.session.add(entity)
    db.session.commit()
    flash(f"Successfully added feedback.", category="success")
    return redirect(url_for('feedback.feedback'))

