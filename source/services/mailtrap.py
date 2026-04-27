from flask import current_app
from flask_mail import Mail, Message

import os
 
class MailtrapHandler():
    def __init__(self):
        self.mail = Mail()

    def send_email(self, subject:str, recipients:str, content:str, content_type:str, sender:str = None):
        """
        Sends an email with the specified content.

        Args:
            subject (str): The subject of the email.
            recipients (str): The recipient's email address or a list of recipients.
            content (str): The content of the email, which can be plain text or HTML.
            content_type (str): The content type, "text" for plain text, "html" for HTML.
            sender (str): The sender's email address.

        Returns:
            None

        Raises:
            ValueError: If content_type is not "text" or "html".

        Note:
            If sender is None, the default email address configured in MAIL_DEFAULT_SENDER will be used.

        Example:
            send_email("My Subject", "sender@example.com", "recipient@example.com", "This is a test email", "text")
        """
        try:
            if sender is None:
                sender = os.getenv("MAIL_DEFAULT_SENDER")

            msg = Message(subject,
                        sender=sender,
                        recipients=[recipients])

            if content_type == "text":
                msg.body = content
            elif content_type == "html":
                msg.html = content
            else:
                raise ValueError("content_type must be 'text' or 'html'.")
            
            self.mail.send(msg)
        except Exception as exception:
            current_app.logger.info(f"Error sending a email: {exception}")
            raise exception

mail = Mail()
mailtrap = MailtrapHandler()