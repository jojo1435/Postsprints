from flask_wtf import FlaskForm

from wtforms import BooleanField, EmailField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

import re

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

    def validate_password(self, field):
        """Require at least one uppercase, one lowercase, one digit."""
        pw = field.data or ""
        if not re.search(r"[A-Z]", pw):
            raise ValidationError("Must include at least one uppercase letter.")
        if not re.search(r"[a-z]", pw):
            raise ValidationError("Must include at least one lowercase letter.")
        if not re.search(r"\d", pw):
            raise ValidationError("Must include at least one number.")
        

    confirm_password = PasswordField("Confirm Password", validators=[
        DataRequired(),
        Length(min=8, max=72),
        EqualTo("password", message="Passwords must match")
    ])
    accept = BooleanField(default=False, validators=[DataRequired(message="You must accept the terms and conditions")])
    remember = BooleanField("Remember Me", default=True)
    submit = SubmitField("Sign Up")