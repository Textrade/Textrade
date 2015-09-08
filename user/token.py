from itsdangerous import URLSafeSerializer, BadSignature

from Textrade import app


def generate_confirmation_token(email):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=3600):
    serializer = URLSafeSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
            token,
            salt=app.config['SECURITY_PASSWORD_SALT'],
            max_age=expiration
        )
    except BadSignature:
        return False

    return email
