import datetime

from app.core.models import db, BaseModel
from app.user.models import User


class BookCondition(BaseModel, db.Model):
    """Book condition model."""
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(255), unique=True)
    label = db.Column(db.String(255))

    def __init__(self, condition, label=None):
        self.condition = condition
        self.label = label

    def __repr__(self):
        return "<Book Condition: {}>".format(self.condition)

    @staticmethod
    def get_by_id(pk):
        return BookCondition.query.get(pk)


class BookStatus(BaseModel, db.Model):
    """BookStatus model."""
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), unique=True)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return "<BookStatus: {}>".format(self.status)

    @staticmethod
    def get_by_id(pk):
        return BookStatus.query.get(pk)


class BookToRent(BaseModel, db.Model):
    """BookToRent model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    isbn = db.Column(db.String(255))
    condition_id = db.Column(db.Integer, db.ForeignKey('book_condition.id'),
                             nullable=False)
    condition = db.relationship(BookCondition.__name__,
                                backref=db.backref('book_to_rent', lazy='dynamic'))
    condition_comment = db.Column(db.String(255))
    marks = db.Column(db.Boolean)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship(User.__name__,
                           backref=db.backref('book_to_rent', lazy='dynamic'))
    book_status_id = db.Column(db.Integer, db.ForeignKey('book_status.id'),
                               nullable=False)
    book_status = db.relationship(BookStatus.__name__,
                                  backref=db.backref('book_to_rent', lazy='dynamic'))
    added = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, author, description, isbn, condition, comment, marks,
                 user, book_status):
        self.name = name
        self.author = author
        self.description = description
        self.isbn = isbn
        self.condition = condition
        self.condition_id = condition.id
        self.condition_comment = comment
        self.marks = marks
        self.user = user
        self.user_id = user.id
        self.book_status = book_status
        self.book_status_id = book_status.id

    def __repr__(self):
        return "<Book To Rent: {}>".format(self.name)

    def get_listed_date(self):
        return self.added.strftime("%m/%d/%Y")


class BookRenting(BaseModel, db.Model):
    """BookRenting model. This table is for book that user are currently renting."""
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_to_rent.id'), nullable=False)
    book = db.relationship(BookToRent.__name__,
                           backref=db.backref('book_renting', lazy='dynamic'))
    renter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rentee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rented_date = db.Column(db.DateTime, default=datetime.datetime.now())
    returning_date = db.Column(db.DateTime,
                               default=datetime.datetime.now() + datetime.timedelta(weeks=18))

    def __init__(self, book, renter_id, rentee_id):
        self.book = book
        self.book_id = book.id
        self.renter_id = renter_id
        self.rentee_id = rentee_id

    @staticmethod
    def create_from_request(renting_request):
        return BookRenting(
            renting_request.book,
            renting_request.renter_id,
            renting_request.rentee_id
        ).create()

    def __repr__(self):
        return "<BookRenting: {} - {} <-> {}>".format(
            self.book, self.renter_id, self.rentee_id
        )

    def get_due_date(self):
        return self.returning_date.strftime("%m/%d/%Y")


class BookRentingRequest(BaseModel, db.Model):
    """BookRenting model. This table will hold information of a pre-book-renting"""

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book_to_rent.id'), nullable=False)
    book = db.relationship(BookToRent.__name__,
                           backref=db.backref('book_renting_request_book', lazy='dynamic'))
    renter_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rentee_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_requested = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, book, renter, rentee):
        self.book = book
        self.book_id = book.id
        self.renter_id = renter.id
        self.rentee_id = rentee.id

    def __repr__(self):
        return "<BookRenting: {} - {} <-> {}>".format(
            self.book, self.renter_id, self.rentee_id
        )


class BookTradeHave(BaseModel, db.Model):
    """
        BookTradeHave model. This model holds information about
    a book that the user have. For example, this will be a book
    that the user owns and plans to trade it for another book.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    isbn = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User.__name__,
                           backref=db.backref('book_trade_have', lazy='dynamic'))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, isbn, user):
        self.name = name
        self.isbn = isbn
        self.user = user
        self.user_id = user.id

    def __repr__(self):
        return "<BookTradeHave: {}>".format(self.isbn)


class BookTradeWant(BaseModel, db.Model):
    """
        BookTradeWant model. This model holds information about
    a book that the user want. For example, this will be a book
    that the user is will to receive by trading one of the books
    that he/she owns.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    isbn = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User.__name__,
                           backref=db.backref('book_trade_want', lazy='dynamic'))
    date_posted = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, name, isbn, user):
        self.name = name
        self.isbn = isbn
        self.user = user
        self.user_id = user.id

    def __repr__(self):
        return "<BookTradeWant: {}>".format(self.isbn)