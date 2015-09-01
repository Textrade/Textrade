import datetime

from peewee import *
from flask.ext.login import UserMixin

db = MySQLDatabase()


class User(UserMixin, Model):
    """User model."""
    first_name = CharField(max_length=255)
    second_name = CharField(max_length=255)
    username = CharField(max_length=255)
    password = CharField(max_length=255)
    joined = DateTimeField(default=datetime.datetime.now)
    university_name = CharField(max_length=255, null=True)
    university_email = CharField(max_length=255)
    personal_email = CharField(max_length=255)

    class Meta:
        database = db

