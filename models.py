import datetime

from flask.ext.login import UserMixin
from peewee import *
from flask.ext.bcrypt import generate_password_hash


# DATABASE INFO
HOST = "localhost"
DATABASE_NAME = "textrade"
PORT = 3306
USERNAME = "root"
PASSWORD = ""

db = MySQLDatabase(DATABASE_NAME, host=HOST, port=PORT,
                   user=USERNAME, passwd=PASSWORD)


class UserRole(Model):
    """User role table. Used to have restriction for users."""
    role = CharField(max_length=40, unique=True)

    class Meta:
        database = db

    def __str__(self):
        return self.role


class User(UserMixin, Model):
    """User model."""
    first_name = CharField(max_length=255)
    last_name = CharField(max_length=255)
    username = CharField(max_length=255, unique=True)
    password = CharField(max_length=255)
    joined = DateTimeField(default=datetime.datetime.now)
    # TODO: when expansion to different schools
    # university_name = CharField(max_length=255)
    university_email = CharField(max_length=255)
    personal_email = CharField(max_length=255, null=True)
    role = ForeignKeyField(UserRole, to_field='role', related_name='user', default='costumer')
    active = BooleanField(default=False)
    activated_on = DateField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name)


class TradeStatus(Model):
    """Status for trades"""
    status = CharField(max_length=50, unique=True)

    class Meta:
        database = db

    def __str__(self):
        return self.status


class BookStatus(Model):
    """Status for books"""
    status = CharField(max_length=50, unique=True)

    class Meta:
        database = db

    def __str__(self):
        return self.status


class Book(Model):
    """Book model."""
    name = CharField(max_length=255)
    edition = CharField(max_length=255)
    author = CharField(max_length=255)
    isbn = CharField(max_length=255, unique=True)
    username = ForeignKeyField(User, to_field='username', related_name='book')
    available = ForeignKeyField(BookStatus, to_field='status', related_name='book')
    added = DateField(default=datetime.datetime.now)
    
    class Meta:
        database = db

    def __str__(self):
        return self.name


class Trade(Model):
    """Trade model."""
    user_one = ForeignKeyField(User, to_field='username', related_name='user_one')
    user_two = ForeignKeyField(User, to_field='username', related_name='user_two')
    book_one = ForeignKeyField(Book, to_field='isbn', related_name='book_one_to_trade')
    book_two = ForeignKeyField(Book, to_field='isbn', related_name='book_two_to_trade')
    status = ForeignKeyField(TradeStatus, to_field='status', related_name='trade')
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return "Trade between {} and {}".format(self.user_one, self.user_two)


class WishList(Model):
    """WishList model."""
    book = ForeignKeyField(Book, to_field='isbn')
    username = ForeignKeyField(User, to_field='username')
    status = CharField(max_length=255)
    date = DateTimeField()

    class Meta:
        database = db

    def __str__(self):
        return "{} Wish List".format(self.username)


def create_tables():
    """Create tables from model"""
    db.connect()
    try:
        db.create_tables(
            [
                UserRole,
                User,
                TradeStatus,
                BookStatus,
                Book,
                Trade,
                WishList,
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
                UserRole,
                User,
                TradeStatus,
                BookStatus,
                Book,
                Trade,
                WishList
            ]
        )


def init_app():
    """Create rows for default foreignkey."""
    user_role = [
        {'role': 'admin'},
        {'role': 'developer'},
        {'role': 'costumer'},
    ]
    book_status = [
        {'status': 'requested'},
        {'status': 'no_available'},
        {'status': 'available'},
    ]
    trade_status = [
        {'status': 'completed'},
        {'status': 'processing'},
        {'status': 'cancelled'},
    ]

    with db.atomic():
        UserRole.insert_many(user_role).execute()
        BookStatus.insert_many(book_status).execute()
        TradeStatus.insert_many(trade_status).execute()
    User.create(
        first_name="admin", last_name="admin",
        username="admin", password=generate_password_hash("admin"),
        university_email="admin@student.uml.edu", role="admin",
        active=True
    )

if __name__ == '__main__':
    drop_tables()
    create_tables()
    init_app()
