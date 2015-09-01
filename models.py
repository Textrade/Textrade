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


class Trade(Model):
    """Trade model."""
    user_one = ForeignKeyField(User, to_field='username')
    user_two = ForeignKeyField(User, to_field='username')
    book = ForeignKeyField(Book, to_field='isbn')
    status = CharField(max_length=255)
    date = DateField(default=datetime.datetime.now)

    class Meta:
        database = db


class WishList(Model):
    """WishList model."""
    book = ForeignKeyField(Book, to_field='isbn')
    username = ForeignKeyField(User, to_field='username')
    status = CharField(max_length=255)
    date = DateTimeField()

    class Meta:
        database = db


def create_tables():
    """Create tables from model"""
    db.connect()
    try:
        db.create_tables(
            [
                User,
                Book,
                Trade,
                WishList
            ],
            safe=True
        )
    except Exception as e:
        print(e)
        return None
    db.close()
    print("Tables created successfully.")


def drop_tables():
    """Delete all tables of the model."""
    print("All the information in the tables will be gone.")
    choice = input("Are you sure? [y/N] >>> ").upper()
    if choice == 'Y':
        db.connect()
        db.drop_tables(
            [
                WishList,
                Trade,
                Book,
                User
            ]
        )


if __name__ == '__main__':
    create_tables()
