from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField, RadioField, EmailField, DateField, FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.domain.Todo import *
from app.domain.Feedback import *
from app.domain.User import *
class LoginForm(FlaskForm):
    login = StringField("Login",
                        render_kw={"placeholder": "Login"},
                        validators=[
                            DataRequired(message="Your login cannot be empty.")
                        ])
    password = PasswordField("Password",
                             render_kw={"placeholder": "Password"},
                             validators=[
                                 DataRequired(message="Your password cannot be empty.")
                             ])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Sign in")

class RegisterForm(FlaskForm):
    username = StringField("Username",
                           render_kw={'placeholder': 'Username'},
                           validators=[
                               DataRequired(message="Username is required."),
                               Regexp("^[A-Za-z0-9\\._\\-]*$", 0,
                                      'Username should have letters, numbers, underscores, dots')
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
                                DataRequired(message="Last name required."),
                                Regexp('^[A-Z]{1}[a-z]*$', 0,
                                       'Last name contains letters with the first one capitalized')
                            ])
    email = EmailField('Email',
                       render_kw={'placeholder': 'Email'},
                       validators=[
                           DataRequired(message="Email required.")
                       ])
    password = PasswordField('Password',
                             render_kw={'placeholder': 'Password'},
                             validators=[
                                 DataRequired(message="Password required."),
                                 Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$', 0,
                                        'Password must contain AT LEAST eight characters, one uppercase letter, one lowercase letter and one number!')
                             ])
    confirm_password = PasswordField('Confirm password',
                                    render_kw={'placeholder': 'Confirm password'},
                                    validators=[
                                        DataRequired(message="Confirm password required."),
                                        EqualTo('password')
                                    ])
    user_image = FileField('Profile picture',
                           render_kw={'placeholder': 'Profile picture image', 'accept': '.jpg, .jpeg, .png'})
    submit = SubmitField("Submit")

    def validate_username(self, field):
        if User.query.filter(User.username == field.data).first():
            raise ValidationError('Username already exists.')

    def validate_email(self, field):
        if User.query.filter(User.email == field.data).first():
            raise ValidationError('Email already exists.')

class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password",
                                render_kw={"placeholder": "Old Password"},
                                validators=[
                                    DataRequired(message="Password cannot be empty.")
                                ])
    new_password = PasswordField("New Password",
                                render_kw={"placeholder": "New Password"},
                                validators=[
                                     DataRequired(message="Password cannot be empty."),
                                     Regexp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)[a-zA-Z\\d]{8,}$', 0,
                                        'Password must contain AT LEAST eight characters, one uppercase letter, one lowercase letter and one number!')
                                ])

    submit = SubmitField("Submit")
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