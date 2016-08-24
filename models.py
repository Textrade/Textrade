import datetime

from flask.ext.login import UserMixin
from flask.ext.bcrypt import generate_password_hash
from flask_sqlalchemy import SQLAlchemy


# class TradeStatus(Model):
#     """Status for trades"""
#     status = CharField(max_length=50, unique=True)
#
#     class Meta:
#         database = db
#
#     def __str__(self):
#         return "<TradeStatus Model: {}>".format(self.status)
#
# class Trade(Model):
#     """Trade model."""
#     internal_id = CharField(max_length=255, unique=True)
#     user_one = ForeignKeyField(User, to_field='username', related_name='user_one')
#     user_two = ForeignKeyField(User, to_field='username', related_name='user_two')
#     user_one_approved = BooleanField(default=False)
#     user_two_approved = BooleanField(default=False)
#     book_one = CharField(max_length=255, null=False)
#     book_two = CharField(max_length=255, null=False)
#     status = ForeignKeyField(TradeStatus, to_field='status', related_name='trade')
#     date = DateTimeField(default=datetime.datetime.now)
#
#     class Meta:
#         database = db
#
#     def __str__(self):
#         return "<Trade Model: (ID: {} - {} and {})".format(self.id, self.user_one, self.user_two)
#
#     def date_to_formatted_string(self):
#             return self.date.strftime("%m/%d/%Y")
#
#
# class WishList(Model):
#     """WishList model."""
#     book = ForeignKeyField(BookToRent, related_name='book_wishList')
#     username = ForeignKeyField(User, to_field='username')
#     date = DateTimeField(default=datetime.datetime.now)
#
#     class Meta:
#         database = db
#
#     def __str__(self):
#         return "{} Wish List".format(self.username)
#
#
# def create_tables():
#     """Create tables from model"""
#     db.connect()
#     try:
#         db.create_tables(
#             [
#                 UserRole,
#                 User,
#                 TradeStatus,
#                 BookStatus,
#                 BookCondition,
#                 BookToRent,
#                 BookRenting,
#                 BookRentingRequest,
#                 BookTradeWant,
#                 BookTradeHave,
#                 Trade,
#                 WishList,
#             ],
#             safe=True
#         )
#     except Exception as e:
#         print(e)
#         return None
#     db.close()
#     print("Tables created successfully.")
#
#
# def drop_tables():
#     """Delete all tables of the model."""
#     print("All the information in the tables will be gone.")
#     choice = input("Are you sure? [y/N] >>> ").upper()
#     if choice == 'Y':
#         db.connect()
#         db.drop_tables(
#             [
#                 UserRole,
#                 User,
#                 TradeStatus,
#                 BookStatus,
#                 BookCondition,
#                 BookRentingRequest,
#                 BookRenting,
#                 BookToRent,
#                 BookTradeWant,
#                 BookTradeHave,
#                 Trade,
#                 WishList
#             ], safe=True
#         )
#     print("Tables deleted.")
#
#
# def create_trade_data():
#     db.drop_tables(
#         [BookTradeWant, BookTradeHave],
#         safe=True
#     )
#     db.create_tables(
#         [BookTradeHave, BookTradeWant],
#         safe=True
#     )
#
#     users = [
#         'dsantosp12',
#         'jsmith',
#         'myork',
#         'admin',
#     ]
#
#     books = [
#         [
#             ('Physics for Scientists & Engineers: '
#              'A Strategic Approach Plus'),
#             '9780321740908',
#         ],
#         [
#             'Java How To Program', '9780133807806',
#         ],
#         [
#             'Absolute C++', '9780133970784',
#         ],
#         [
#             'Glencoe Health, a Guide to Wellness',
#             '0026515628',
#         ],
#         [
#             ('Manufacturing Planning and Control '
#              'for Supply Chain Management'),
#             '0072299908',
#         ],
#         [
#             ('Principles of Environmental Engineering '
#              'and Science'),
#             '0072350539',
#         ],
#         [
#             'Viscous Fluid Flow', '0072402318',
#         ],
#         [
#             'Biology', '0072437316',
#         ]
#     ]
#
#     want_books = [
#         {
#             'name': books[0][0],
#             'isbn': books[0][1],
#             'user': users[0],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(20))
#         },
#         {
#             'name': books[1][0],
#             'isbn': books[1][1],
#             'user': users[1],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(10))
#         },
#         {
#             'name': books[2][0],
#             'isbn': books[2][1],
#             'user': users[2],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(30))
#         },
#         {
#             'name': books[3][0],
#             'isbn': books[3][1],
#             'user': users[3],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(15))
#         },
#     ]
#
#     have_books = [
#         {
#             'name': books[1][0],
#             'isbn': books[1][1],
#             'user': users[0],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(20))
#         },
#         {
#             'name': books[0][0],
#             'isbn': books[0][1],
#             'user': users[1],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(10))
#         },
#         {
#             'name': books[3][0],
#             'isbn': books[3][1],
#             'user': users[2],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(20))
#         },
#         {
#             'name': books[2][0],
#             'isbn': books[2][1],
#             'user': users[3],
#             'date_posted': (datetime.datetime.now() -
#                             datetime.timedelta(28))
#         },
#     ]
#
#     try:
#         with db.atomic():
#             BookTradeWant.insert_many(want_books).execute()
#             BookTradeHave.insert_many(have_books).execute()
#
#     except Exception as e:
#         print("Something went wrong initializing the book for trade")
#         print(e)
#         return
#     db.close()
#     print("Trade successfully initialized.")
#
#
# def init_app():
#     """Create rows for default foreignkey."""
#     # SETUP TESTING ENVIRONMENT
#     user_role = [
#         {'role': 'admin'},
#         {'role': 'developer'},
#         {'role': 'costumer'},
#     ]
#     book_status = [
#         {'status': 'requested'},
#         {'status': 'no_available'},
#         {'status': 'available'},
#         {'status': 'rented'},
#     ]
#     trade_status = [
#         {'status': 'completed'},
#         {'status': 'processing'},
#         {'status': 'cancelled'},
#     ]
#     users = [
#         {
#             'first_name': 'John',
#             'last_name': 'Smith',
#             'username': 'jsmith',
#             'password': generate_password_hash('test'),
#             'university_email': 'john_smith@student.uml.edu',
#             'personal_email': 'jsmith@gmail.com',
#             'role': 'costumer',
#             'active': True,
#         },
#         {
#             'first_name': 'Marie',
#             'last_name': 'York',
#             'username': 'myork',
#             'password': generate_password_hash('test'),
#             'university_email': 'marie_york@student.uml.edu',
#             'personal_email': 'myork@gmail.com',
#             'role': 'costumer',
#             'active': True,
#         },
#         {
#             'first_name': 'Juan',
#             'last_name': 'Cook',
#             'username': 'jcook',
#             'password': generate_password_hash('test'),
#             'university_email': 'juan_cook@student.uml.edu',
#             'personal_email': 'jcook@gmail.com',
#             'role': 'costumer',
#             'active': True,
#         }
#     ]
#     books_condition = [
#         {
#             'condition': 'Like New',
#             'label': '',
#         },
#         {
#             'condition': 'Very Good',
#             'label': 'Minimal wear on cover, otherwise perfect',
#         },
#         {
#             'condition': 'Good',
#             'label': 'Some wear on the cover, spine, and pages',
#         },
#         {
#             'condition': 'Fair',
#             'label': 'Noticeable wear on the cover, spine and pages',
#         },
#         {
#             'condition': 'Bad',
#             'label': 'Clear evidence of heavy use',
#         },
#     ]
#     rent_books = [
#         {
#             'name': 'Java How To Program',
#             # 'edition': '10th',
#             'author': 'Paul Deitel & Harvey Daitel',
#             'description': 'Init',
#             'isbn': '9780133807806',
#             'username': 'jsmith',
#             'available': 'available',
#             'condition': 'Fair',
#             # 'image_path': 'empty1',
#         },
#         {
#             'name': 'Physics For Scientist and Engineers',
#             # 'edition': '3rd',
#             'author': 'Randall D. Knight',
#             'description': 'Init',
#             'isbn': '978032175291',
#             'username': 'jsmith',
#             'available': 'available',
#             'condition': 'Good',
#             # 'image_path': 'empty3',
#         },
#         {
#             'name': 'MICROECONOMICS PRINCIPLES and POLICY',
#             # 'edition': '13th',
#             'author': 'William J. Baumol & Alan S. Blinder',
#             'description': 'Init',
#             'isbn': '9781305280618',
#             'username': 'myork',
#             'available': 'available',
#             'condition': 'Like New',
#             # 'image_path': 'empty2',
#         },
#         {
#             'name': 'Physics For Scientist and Engineers',
#             # 'edition': '3rd',
#             'author': 'Randall D. Knight',
#             'description': 'Init',
#             'isbn': '978032175291',
#             'username': 'jcook',
#             'available': 'available',
#             'condition': 'Bad',
#             # 'image_path': 'empty4',
#         },
#     ]
#     try:
#         with db.atomic():
#             UserRole.insert_many(user_role).execute()
#             BookStatus.insert_many(book_status).execute()
#             BookCondition.insert_many(books_condition).execute()
#             TradeStatus.insert_many(trade_status).execute()
#             User.insert_many(users).execute()
#             BookToRent.insert_many(rent_books).execute()
#         User.create(
#             first_name="admin", last_name="admin",
#             username="admin", password=generate_password_hash("admin"),
#             university_email="admin@student.uml.edu", role="admin",
#             active=True
#         )
#
#         create_trade_data()
#
#     except Exception as e:
#         print(e)
#         return
#     print("App initialized successfully.")


if __name__ == '__main__':
    # drop_tables()
    # create_tables()
    # init_app()
    # db.connect()
    # db.drop_table(Trade)
    # db.create_table(Trade)
    # db.close()
    # create_trade_data()
    db.create_all()
