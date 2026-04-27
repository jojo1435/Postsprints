from functools import wraps
from flask_login import current_user
from flask import redirect, url_for

def anonymous_required(func):
    """
    Decorator that restricts access to routes for authenticated users.

    This decorator ensures that only anonymous (non-authenticated) users
    can access the decorated route. If the current user is already
    authenticated, they will be redirected to the dashboard index page.

    Args:
        func (Callable): The view function to decorate.

    Returns:
        Callable: The wrapped view function that performs the authentication check.

    Behavior:
        - If `current_user.is_authenticated` is True, the user is redirected
          to the "dashboard.index" route.
        - Otherwise, the original view function is executed normally.

    Example:
        @auth.route("/signin", methods=["GET", "POST"])
        @anonymous_required
        def signin():
            return render_template("signin.html")

        In this example, authenticated users attempting to access the
        signin page will be redirected to the homepage.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for("dashboard.index"))
        return func(*args, **kwargs)
    return decorated_function

def active_user_required(func):
    """
    Decorator that restricts access to users whose accounts are not activated.

    This decorator ensures that only users with an active account
    (`current_user.is_verified == True`) can access the decorated route.
    If the user's account is not activated, they will be redirected
    to the email verification page.

    Args:
        func (Callable): The view function to decorate.

    Returns:
        Callable: The wrapped view function that performs the activation check.

    Behavior:
        - If `current_user.is_authenticated` and `current_user.is_verified` is False,
          the user is redirected to the "auth.verify" route.
        - Otherwise, the original view function is executed normally.

    Example:
        @dashboard.route("/dashboard")
        @login_required
        @active_user_required
        def dashboard():
            return render_template("dashboard.html")

        In this example, users who are logged in but have not verified
        their email will be redirected to the verification page.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated and not current_user.is_verified:
            return redirect(url_for("auth.verify"))
        return func(*args, **kwargs)

    return decorated_function