from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required, login_user, logout_user, current_user

from config import MAIL_SUPPORT_SENDER

from source.forms.auth import SignInForm, SignUpForm
from source.models.plan import Plan
from source.models.usage import Usage
from source.models.user import User
from source.services.mailtrap import mailtrap
from source.utils.decorators import anonymous_required
from source.utils.login import login_handler

auth = Blueprint("auth", __name__)

@auth.route("/signin", methods=["GET", "POST"])
@anonymous_required
def signin():
    signin_form = SignInForm()

    if signin_form.validate_on_submit():
        email = signin_form.email.data
        password = signin_form.password.data
        remember = signin_form.remember.data

        user = User.get_by_email(email)
        if user is not None:
            if user.check_password(password):
                login_user(user, remember=remember)
                next_page = request.args.get("next")
                return redirect(next_page or url_for("dashboard.index"))
            else:
                signin_form.email.errors.append("Invalid email or password, please try again")
        else:
            signin_form.email.errors.append("Invalid email or password, please try again")

    return render_template("pages/auth/signin.html", 
                           signin_form=signin_form)

@auth.route("/signup", methods=["GET", "POST"])
@anonymous_required
def signup():
    signup_form = SignUpForm()

    if signup_form.validate_on_submit():
        name = signup_form.name.data
        email = signup_form.email.data
        password = signup_form.password.data
        remember = signup_form.remember.data

        user = User.get_by_email(email)
        if user is None:
            user = User(name, email)
            user.set_password(password)
            user.set_plan(Plan.free())
            user.save()
            
            usage = Usage.create_for_user(user.id)
            usage.save()

            login_user(user, remember=remember)

            token = login_handler.generate_confirmation_token(email)
            confirm_url = url_for("auth.confirm_email", token=token, _external=True)
            mailtrap.send_email(
                "Confirm your account",
                email,
                render_template("emails/auth-confirm-password.html", 
                                email = email,
                                confirm_url = confirm_url, 
                                contact_sender = MAIL_SUPPORT_SENDER),
                                "html"
            )
            return redirect(url_for("auth.verify"))
        else:
            signup_form.email.errors.append("This email is already registered by another user")

    return render_template("pages/auth/signup.html", 
                           signup_form=signup_form)

@auth.route("/signout")
@login_required
def signout():
    logout_user()
    return redirect(url_for("main.index"))

@auth.route("/verify-account", methods=["GET"])
@login_required
def verify():
    if current_user.is_verified:
        return redirect(url_for("dashboard.index"))
    else:
        return render_template("pages/auth/verify.html")

@auth.route("/confirm/account/token/<string:token>", methods=["GET"])
@login_required
def confirm_email(token):
    email = login_handler.confirm_token(token)
    if email:
        current_user.confirm_user()
        return redirect(url_for("dashboard.index"))
    else:
        return redirect(url_for("main.index"))