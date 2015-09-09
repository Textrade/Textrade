from itsdangerous import URLSafeSerializer, BadSignature
from flask.ext.mail import Message
from Textrade import app, mail


def generate_confirmation_token(email):
    """Generate confirmation token."""
    serializer = URLSafeSerializer(secret_key=app.config['SECRET_KEY'])
    return serializer.dumps(email, salt='1234')


def confirm_token(token, expiration=3600):
    """Check for the confirmation token."""
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt='1234'
        )
    except BadSignature:
        return False
    return email


def send_email(to, subject, template):
    """Send an email"""
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=app.config['MAIL_SENDER']
    )
    mail.send(msg)
