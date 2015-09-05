import datetime

from models import User, db


def create_user(**kwargs):
    """"Create user controls."""
    User.create(
        first_name=kwargs['first_name'],
        last_name=kwargs['last_name'],
        username=kwargs['username'],
        password=kwargs['password'],
        # university_name=kwargs['university_name'],
        university_email=kwargs['university_email'],
        personal_email=kwargs['personal_email']
    )
