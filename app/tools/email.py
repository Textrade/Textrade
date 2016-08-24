from flask import render_template

import config
from app.user.user import UserController

import sendgrid

#
#   DEFAULT EMAILS
#
INFO = "Info <info@textrade.edu>"
NO_REPLY = "No Reply <no_reply@textrade.us>"
SUPPORT = "Support <support@textrade.us>"


class EmailException(Exception):
    pass


class EmailController:
    def __init__(self, html="", subject="",
                 from_user="", to_user="", cc_user=""):
        self.send_grid_client_ = sendgrid.SendGridClient(config.SENDGRID_API_KEY)
        self.mail_ = None
        self.to_user_ = to_user
        self.from_user_ = from_user
        self.cc_user_ = cc_user
        self.subject_ = subject
        self.html_ = html

    def send_activation_email(self, user):
        html = render_template(
            "email/verifyNewAccount/verification.html",
            name="%s %s" % (user['first_name'], user['last_name']),
            token=UserController.generate_token(user['university_email']),
            domain=config.DOMAIN_NAME
        )
        subject = "Confirm email and activate your account!"

        self.mail_ = sendgrid.Mail(
            to=user['university_email'],
            from_email=NO_REPLY,
            subject=subject,
            html=html,
        )
        self.send()

    def send(self):
        if self.mail_ is not None:
            self.send_grid_client_.send(self.mail_)
        else:
            raise EmailException("The email is NoneType")
