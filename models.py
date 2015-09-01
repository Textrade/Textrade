import datetime

from peewee import *
from flask.ext.login import UserMixin


# DATABASE INFO
HOST = "localhost"
DATABASE_NAME = "textrade"
PORT = 3306
USERNAME = "root"
PASSWORD = ""

db = MySQLDatabase(DATABASE_NAME, host=HOST, port=PORT,
                   user=USERNAME, passwd=PASSWORD)


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


class Book(Model):
    """Book model."""
    name = CharField(max_length=255)
    edition = CharField(max_length=255)
    author = CharField(max_length=255)
    isbn = CharField(max_length=255)
    username = CharField(max_length=255)
    available = CharField(max_length=255)
    added = DateField(default=datetime.datetime.now)

    class Meta:
        database = db
