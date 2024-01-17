from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length
class LoginForm(FlaskForm):
    login = StringField("Login",
                        render_kw={"placeholder": "Login"},
                        validators=[
                            DataRequired(message="Your login cannot be empty.")
                        ])
    password = PasswordField("Password",
                             render_kw={"placeholder": "Password"},
                             validators=[
                                 DataRequired(message="Your password cannot be empty."),
                                 Length(min=4, max=10)
                             ])
    remember = BooleanField("Remember", default=False)
    submit = SubmitField("Sign in")
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField("Old Password",
                                 render_kw={"placeholder": "Old Password"},
                                 validators=[
                                     DataRequired(message="Password cannot be empty."),
                                     Length(min=4, max=10)
                                 ])
    new_password = PasswordField("New Password",
                                 render_kw={"placeholder": "New Password"},
                                 validators=[
                                     DataRequired(message="Password cannot be empty."),
                                     Length(min=4, max=10)
                                 ])
    submit = SubmitField("Submit")
class AddTask(FlaskForm):
    name = StringField("Name",
                       render_kw={"placeholder": "Task name"},
                       validators=[
                           DataRequired(message="Task name required.")
                       ])
    description = TextAreaField("Description", render_kw={"placeholder": "Description"})


class UpdateTask(FlaskForm):
    name = StringField("Name",
                       render_kw={"placeholder": "Task name"},
                       validators=[
                           DataRequired(message="Task name required.")
                       ])
    description = TextAreaField("Description", render_kw={"placeholder": "Description"})
    status = SelectField("Status", choices=Status.get_dropdown_values())