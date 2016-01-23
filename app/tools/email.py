from flask import render_template
from flask.ext.mail import Message

from app import app
from config import DOMAIN_NAME
from app.user.user import UserController


class EmailController:
    def __init__(self, mail):
        self.mail = mail

    def send_activation_email(self, user):
        HTML = render_template(
            "email/verifyNewAccount/verification.html",
            name="%s %s" % (user['first_name'], user['last_name']),
            token=UserController.generate_token(user['university_email']),
            domain=DOMAIN_NAME
        )
        SUBJECT = "Confirm email and activate your account!"
        self.mail.send(
            Message(subject=SUBJECT, recipients=[user['university_email']],
                    html=HTML, sender=app.config['MAIL_SENDER'])
        )
