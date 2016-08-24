from flask import render_template

from app import app
from config import DOMAIN_NAME
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
        self.send_grid_client_ = sendgrid.SendGridClient(
            ('SG.5I_F7IejRiSDZJEyjKBO9w.qwnuDNJMEFt'
             'XZEQdllPSuPqB2ZyjZvied4H7hayNJt4')
        )
        self.mail_ = None
        self.to_user_ = to_user
        self.from_user_ = from_user
        self.cc_user_ = cc_user
        self.subject_ = subject
        self.html_ = html

    def send_activation_email(self, user):
        HTML = render_template(
            "email/verifyNewAccount/verification.html",
            name="%s %s" % (user['first_name'], user['last_name']),
            token=UserController.generate_token(user['university_email']),
            domain=DOMAIN_NAME
        )
        SUBJECT = "Confirm email and activate your account!"

        self.mail_ = sendgrid.Mail(
            to=self.to_user_,
            from_email=NO_REPLY,
            subject=SUBJECT,
            html=HTML,
        )
        self.mail_.send()

    def send(self):
        if self.mail_ is not None:
            self.send_grid_client_.send(self.mail_)
        else:
            raise EmailException("The email is NoneType")

    """
    self.mail_.add_to(self.to_user_)
        self.mail_.add_cc(self.cc_user_)
        self.mail_.set_subject(self.subject_)
        self.mail_.set_html(self.html_)
        self.mail_.set_from(self.from_user_)
        self.send_grid_client_.send(self.mail_)
    """
