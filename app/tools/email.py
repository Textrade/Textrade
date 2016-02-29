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
    def __init__(self):
        self.sg = sendgrid.SendGridClient(
            ('SG.5I_F7IejRiSDZJEyjKBO9w.qwnuDNJMEFt'
             'XZEQdllPSuPqB2ZyjZvied4H7hayNJt4')
        )
        self.message = sendgrid.Mail()

    def send_test(self, email):
        self.message.add_to(email)
        self.message.set_subject("Textrade")
        self.message.set_html("<h1>Big hi, the test works!</h1>")
        self.message.set_from("Joseph Meli <joseph.meli@textrade.us>")
        self.sg.send(self.message)
