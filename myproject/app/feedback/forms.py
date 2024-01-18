from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField, RadioField, EmailField, DateField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.domain.Todo import Status
from app.domain.Feedback import Satisfaction
from app.domain.User import User
from flask_login import current_user



class AddFeedback(FlaskForm):
    feedback = TextAreaField("Feedback",
                             render_kw={'placeholder': 'Give feedback'},
                             validators=[
                                 DataRequired(message="Feedback required.")
                             ])
    satisfaction = RadioField("Satisfaction",
                              choices=[(satisfaction.name, satisfaction.value.lower().capitalize()) for satisfaction in Satisfaction],
                              validators=[
                                  DataRequired(message="Rate your experience.")
                              ])
    submit = SubmitField("Submit")