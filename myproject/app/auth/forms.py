from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, EmailField,  FileField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp

from app.domain.User import User

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
