import datetime

from flask.ext.login import UserMixin
from peewee import *
from flask.ext.bcrypt import generate_password_hash

# DATABASE INFO
HOST = "us-cdbr-iron-east-03.cleardb.net"
DATABASE_NAME = "heroku_b0692bbbba2a643"
PORT = 3306
USERNAME = "b366db0b05b78c"
PASSWORD = "3a9b0e26"
#
# HOST = "localhost"
# DATABASE_NAME = "textrade2"
# USERNAME = "root"
# PASSWORD = ""

db = MySQLDatabase(DATABASE_NAME, host=HOST, port=PORT,
                   user=USERNAME, passwd=PASSWORD)


class UserRole(Model):
    """User role table. Used to have restriction for users."""
    role = CharField(max_length=40, unique=True)

    class Meta:
        database = db

    def __str__(self):
        return self.role


# TODO: Review system.
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
    activated_on = DateTimeField(null=True)

    class Meta:
        database = db

    def __str__(self):
        return "<User Model: {}>".format(self.username)

    def get_name(self):
        return "{} {}".format(self.first_name, self.last_name)

    def joined_to_string(self):
        return self.joined.strftime("%b. %Y")


class TradeStatus(Model):
    """Status for trades"""
    status = CharField(max_length=50, unique=True)

    class Meta:
        database = db

    def __str__(self):
        return "<TradeStatus Model: {}>".format(self.status)


class BookStatus(Model):
    """Status for books"""
    status = CharField(max_length=50, unique=True)

    class Meta:
        database = db

    def __str__(self):
        return "<BookStatus Model: {}>".format(self.status)


class BookCondition(Model):
    """List of condition for the books."""
    condition = CharField(max_length=255, unique=True)
    label = CharField(max_length=255)

    class Meta:
        database = db

    def __str__(self):
        return "<BookCondition Model: {}>".format(self.condition)


class BookToRent(Model):
    """BookToRent model."""
    name = CharField(max_length=255)
    # edition = CharField(max_length=255)
    author = CharField(max_length=255)
    description = TextField()
    isbn = CharField(max_length=255)
    condition = ForeignKeyField(BookCondition, to_field='condition', related_name='book')
    condition_comment = TextField(default="")
    marks = BooleanField(default=False)
    username = ForeignKeyField(User, to_field='username', related_name='book')
    available = ForeignKeyField(BookStatus, to_field='status', related_name='book')
    added = DateTimeField(default=datetime.datetime.now)
    # image_path = CharField(max_length=255, unique=True)
    
    class Meta:
        database = db

    def __str__(self):
        return "<BookToRent Model: {}>".format(self.name)

    def date_listed(self):
        return self.added.strftime("%m/%d/%Y")

    def get_book_name(self):
        return self.name

    def is_available(self):
        if self.available.status == "available":
            return 1
        return 0


class BookRenting(Model):
    """BookRenting model. This table is for book that users are currently renting."""
    book = ForeignKeyField(BookToRent, to_field='id', related_name='book_for_renting')
    renter = ForeignKeyField(User, to_field='username', related_name='renter_user')
    rentee = ForeignKeyField(User, to_field='username', related_name='rentee_user')
    rented_date = DateTimeField(default=datetime.datetime.now)
    returning_date = DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(weeks=18)))

    class Meta:
        database = db

    def __str__(self):
        return "<BookRenting Model: {} - {} <-> {}>".format(
            self.book, self.renter, self.rentee
        )


class BookRentingRequest(Model):
    """BookRentingRequest model. This table will hold the renting until the renter accept."""
    book = ForeignKeyField(BookToRent, to_field='id', related_name='book_requested')
    renter = ForeignKeyField(User, to_field='username', related_name='renter_requested')
    rentee = ForeignKeyField(User, to_field='username', related_name='user_requesting')
    date_requested = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return "<BookRentingRequest Model: {} - {}>".format(self.book, self.rentee)

    def date_requested_to_string(self):
        return self.date_requested.strftime("%m/%d/%Y")


class BookTradeHave(Model):
    """BookTradeHave model."""
    name = CharField(max_length=255)
    isbn = CharField(max_length=255)
    # TODO: Change to username
    user = ForeignKeyField(User, to_field='username', related_name="book_trade_have")

    class Meta:
        database = db

    def __str__(self):
        return "<BookTradeHave Model: {}>".format(self.isbn)


class BookTradeWant(Model):
    """BookTradeWant model."""
    name = CharField(max_length=255)
    isbn = CharField(max_length=255)
    # TODO: Change to username convention
    user = ForeignKeyField(User, to_field='username', related_name="book_trade_want")

    class Meta:
        database = db

    def __str__(self):
        return "<BookTradeWant Model: {}>".format(self.isbn)


class Trade(Model):
    """Trade model."""
    user_one = ForeignKeyField(User, to_field='username', related_name='user_one')
    user_two = ForeignKeyField(User, to_field='username', related_name='user_two')
    book_one = ForeignKeyField(BookToRent, related_name='book_one_to_trade')
    book_two = ForeignKeyField(BookToRent, related_name='book_two_to_trade')
    status = ForeignKeyField(TradeStatus, to_field='status', related_name='trade')
    date = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db

    def __str__(self):
        return "Trade between {} and {}".format(self.user_one, self.user_two)


class WishList(Model):
    """WishList model."""
    book = ForeignKeyField(BookToRent, related_name='book_wishList')
    username = ForeignKeyField(User, to_field='username')
    date = DateTimeField(default=datetime.datetime.now)

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
                BookCondition,
                BookToRent,
                BookRenting,
                BookRentingRequest,
                BookTradeWant,
                BookTradeHave,
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
                BookCondition,
                BookRentingRequest,
                BookRenting,
                BookToRent,
                BookTradeWant,
                BookTradeHave,
                Trade,
                WishList
            ], safe=True
        )
    print("Tables deleted.")


def init_app():
    """Create rows for default foreignkey."""
    # SETUP TESTING ENVIRONMENT
    user_role = [
        {'role': 'admin'},
        {'role': 'developer'},
        {'role': 'costumer'},
    ]
    book_status = [
        {'status': 'requested'},
        {'status': 'no_available'},
        {'status': 'available'},
        {'status': 'rented'},
    ]
    trade_status = [
        {'status': 'completed'},
        {'status': 'processing'},
        {'status': 'cancelled'},
    ]
    users = [
        {
            'first_name': 'John',
            'last_name': 'Smith',
            'username': 'jsmith',
            'password': generate_password_hash('test'),
            'university_email': 'john_smith@student.uml.edu',
            'personal_email': 'jsmith@gmail.com',
            'role': 'costumer',
            'active': True,
        },
        {
            'first_name': 'Marie',
            'last_name': 'York',
            'username': 'myork',
            'password': generate_password_hash('test'),
            'university_email': 'marie_york@student.uml.edu',
            'personal_email': 'myork@gmail.com',
            'role': 'costumer',
            'active': True,
        },
        {
            'first_name': 'Juan',
            'last_name': 'Cook',
            'username': 'jcook',
            'password': generate_password_hash('test'),
            'university_email': 'juan_cook@student.uml.edu',
            'personal_email': 'jcook@gmail.com',
            'role': 'costumer',
            'active': True,
        }
    ]
    books_condition = [
        {
            'condition': 'Like New',
            'label': '',
        },
        {
            'condition': 'Very Good',
            'label': 'Minimal wear on cover, otherwise perfect',
        },
        {
            'condition': 'Good',
            'label': 'Some wear on the cover, spine, and pages',
        },
        {
            'condition': 'Fair',
            'label': 'Noticeable wear on the cover, spine and pages',
        },
        {
            'condition': 'Bad',
            'label': 'Clear evidence of heavy use',
        },
    ]
    rent_books = [
        {
            'name': 'Java How To Program',
            # 'edition': '10th',
            'author': 'Paul Deitel & Harvey Daitel',
            'description': 'Init',
            'isbn': '9780133807806',
            'username': 'jsmith',
            'available': 'available',
            'condition': 'Fair',
            # 'image_path': 'empty1',
        },
        {
            'name': 'Physics For Scientist and Engineers',
            # 'edition': '3rd',
            'author': 'Randall D. Knight',
            'description': 'Init',
            'isbn': '978032175291',
            'username': 'jsmith',
            'available': 'available',
            'condition': 'Good',
            # 'image_path': 'empty3',
        },
        {
            'name': 'MICROECONOMICS PRINCIPLES and POLICY',
            # 'edition': '13th',
            'author': 'William J. Baumol & Alan S. Blinder',
            'description': 'Init',
            'isbn': '9781305280618',
            'username': 'myork',
            'available': 'available',
            'condition': 'Like New',
            # 'image_path': 'empty2',
        },
        {
            'name': 'Physics For Scientist and Engineers',
            # 'edition': '3rd',
            'author': 'Randall D. Knight',
            'description': 'Init',
            'isbn': '978032175291',
            'username': 'jcook',
            'available': 'available',
            'condition': 'Bad',
            # 'image_path': 'empty4',
        },
    ]
    try:
        with db.atomic():
            UserRole.insert_many(user_role).execute()
            BookStatus.insert_many(book_status).execute()
            BookCondition.insert_many(books_condition).execute()
            TradeStatus.insert_many(trade_status).execute()
            User.insert_many(users).execute()
            BookToRent.insert_many(rent_books).execute()
        User.create(
            first_name="admin", last_name="admin",
            username="admin", password=generate_password_hash("admin"),
            university_email="admin@student.uml.edu", role="admin",
            active=True
        )
    except Exception as e:
        print(e)
        return
    print("App initialized successfully.")


if __name__ == '__main__':
    drop_tables()
    create_tables()
    init_app()
