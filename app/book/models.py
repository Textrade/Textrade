import datetime

from app.core.models import db, BaseModel
from app.user.models import User


class BookCondition(BaseModel):
    """Book condition model."""
    id = db.Column(db.Integer, primary_key=True)
    condition = db.Column(db.String(255), unique=True)
    label = db.Column(db.String(255))

    def __init__(self, condition, label=None):
        self.condition = condition
        self.label = label

    def __repr__(self):
        return "<Book Condition: {}>".format(self.condition)


class BookStatus(BaseModel):
    """BookStatus model."""
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(255), unique=True)

    def __init__(self, status):
        self.status = status

    def __repr__(self):
        return "<BookStatus: {}>".format(self.status)


class BookToRent(BaseModel):
    """BookToRent model."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    author = db.Column(db.String(255))
    description = db.Column(db.Text)
    isbn = db.Column(db.String(255))
    condition_id = db.Column(db.Integer, db.ForeignKey('book_condition.condition'),
                             nullable=False)
    condition = db.relationship(BookCondition.__name__,
                                backref=db.backref('book_to_rent', lazy='dynamic'))
    condition_comment = db.Column(db.String(255))
    marks = db.Column(db.Boolean)
    username_id = db.Column(db.Integer, db.ForeignKey('user.id'))
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
        self.username_id = user.id
        self.book_status = book_status
        self.book_status_id = book_status.id

    def __repr__(self):
        return "<Book To Rent: {}>".format(self.name)
