from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField, RadioField, EmailField, DateField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.domain.Todo import Status

from app.domain.User import User
from flask_login import current_user


class UpdateUserForm(FlaskForm):
    username = StringField("Username",
                           render_kw={'placeholder': 'Username'},
                           validators=[
                               DataRequired(message="Username can't be empty."),
                               Regexp("^[A-Za-z0-9\\._\\-]*$", 0,
                                      'Username can only contain alphanumericals, underscores and dots')
                           ])
    first_name = StringField("First name",
                             render_kw={'placeholder': 'First name'},
                             validators=[
                                 DataRequired(message="First name is required."),
                                 Regexp('^[A-Z]{1}[a-z]*$', 0,
                                        'First name contains letters with the first one capitalized')
                             ])
    last_name = StringField("Last name",
                            render_kw={'placeholder': 'Last name'},
                            validators=[
                                DataRequired(message="Last name is required."),
                                Regexp('^[A-Z]{1}[a-z]*$', 0,
                                       'Last name contains letters with the first one capitalized')
                            ])
    email = EmailField('Email',
                       render_kw={'placeholder': 'Email'},
                       validators=[
                           DataRequired(message="Email is required.")
                       ])
    user_image = FileField('Avatar',
                           render_kw={'placeholder': 'Avatar', 'accept': '.jpg, .jpeg, .png'})
    about_me = TextAreaField('About me',
                             render_kw={'placeholder': 'About me'})
    submit = SubmitField("Submit")
    def validate_username(self, field):
        if current_user.username != field.data and User.query.filter(User.username == field.data).first():
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        if current_user.email != field.data and User.query.filter(User.email == field.data).first():
            raise ValidationError('Email already exists.')




class AddTask(FlaskForm):
    name = StringField("Name",
                       render_kw={"placeholder": "Task name"},
                       validators=[
                           DataRequired(message="Task name required.")
                       ])
    description = TextAreaField("Description", render_kw={"placeholder": "Description"})
    submit = SubmitField("Add task")


class UpdateTask(FlaskForm):
    name = StringField("Name",
                       render_kw={"placeholder": "Task name"},
                       validators=[
                           DataRequired(message="Task name required.")
                       ])
    description = TextAreaField("Description", render_kw={"placeholder": "Description"})
    status = SelectField("Status", choices=Status.get_dropdown_values())
    submit = SubmitField("Update task")
