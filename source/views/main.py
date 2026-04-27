from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def index():
    if current_user.is_authenticated:
        return "user is loged in"
    else:
        return "user is anonymous"