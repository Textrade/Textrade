from flask import render_template
from flask.ext.mail import Message

from app import app
from config import DOMAIN_NAME
from app.user.user import UserController

import sendgrid


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


class SendGridTest:
    def __init__(self, html="", subject="",
                 from_user="", to_user="", cc_user=""):
        self.sg = sendgrid.SendGridClient(
            ('SG.5I_F7IejRiSDZJEyjKBO9w.qwnuDNJMEFt'
             'XZEQdllPSuPqB2ZyjZvied4H7hayNJt4')
        )
        self.mail_ = sendgrid.Mail()
        self.to_user_ = to_user
        self.from_user_ = from_user
        self.cc_user_ = cc_user
        self.subject_ = subject
        self.html_ = html

    def send(self):
        self.mail_.add_to(self.to_user_)
        self.mail_.add_cc(self.cc_user_)
        self.mail_.set_subject(self.subject_)
        self.mail_.set_html(self.html_)
        self.mail_.set_from(self.from_user_)
        self.sg.send(self.mail_)
