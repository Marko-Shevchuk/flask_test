from flask_wtf import FlaskForm
from wtforms import  SubmitField, PasswordField
from wtforms.validators import DataRequired,  Regexp

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