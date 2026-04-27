from flask_wtf import FlaskForm

from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignInForm(FlaskForm):
    email = EmailField("Email Address", validators=[
        DataRequired(),
        Length(min=5, max=254),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, max=72)
    ])
    remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Sign In")

class SignUpForm(FlaskForm):
    name = StringField("Your Name", validators=[
        DataRequired(),
        Length(min=3, max=30),
    ])
    email = EmailField("Email Address", validators=[
        DataRequired(),
        Length(min=5, max=254),
        Email()
    ])
    password = PasswordField("Password", validators=[
        DataRequired(),
        Length(min=8, max=72)
    ])
    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        Length(min=8, max=72),
        EqualTo("password", message="Passwords must match")
    ])
    remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Sign Up")