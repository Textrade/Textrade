from itsdangerous import URLSafeSerializer, BadSignature
from flask.ext.mail import Message


def generate_confirmation_token(email, secret_key):
    """Generate confirmation token."""
    serializer = URLSafeSerializer(secret_key=secret_key)
    return serializer.dumps(email, salt='1234')


def confirm_token(token, secret_key, expiration=3600):
    """Check for the confirmation token."""
    # TODO: Set expiration time.
    serializer = URLSafeSerializer(secret_key)
    try:
        email = serializer.loads(
            token,
            salt='1234'
        )
    except BadSignature:
        return False
    return email


def send_email(mail, to, subject, template, sender):
    """Send an email"""
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=sender
    )
    mail.send(msg)

if __name__ == '__main__':
    pass
