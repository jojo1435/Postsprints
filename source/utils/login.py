from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_login import LoginManager

from source.models.user import User

import os

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

class LoginHanlder():
    def generate_confirmation_token(self, email:str):
        """
        Generates a unique confirmation token associated with the given email.

        Args:
            email (str): The email address to be associated with the token.

        Returns:
            str: A unique confirmation token.
        """
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        return serializer.dumps(email, salt=os.getenv("SECURITY_PASSWORD_SALT"))

    def confirm_token(self, token:str, expiration:int=3600):
        """
        Verifies the provided token and retrieves the associated email.

        Args:
            token (str): The token to be verified.
            expiration (int): The expiration time for the token (in seconds). Default is 3600 seconds (1 Hour).

        Returns:
            Union[str, bool]: If the token is valid and within the expiration time, returns the associated email.
                            If the token is invalid or expired, returns False.
        """
        serializer = URLSafeTimedSerializer(os.getenv("SECRET_KEY"))
        try:
            email = serializer.loads(
                token,
                salt=os.getenv("SECURITY_PASSWORD_SALT"),
                max_age=expiration
            )
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return email
    
login_handler = LoginHanlder()