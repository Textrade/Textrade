import datetime

from app import db


class TradeWantBook:
    """Trade want model"""
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.Integer, db.ForeignKey('book.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, book, user, posted):
        self.book = book
        self.user = user
        self.posted = posted

    def __repr__(self):
        return "<TradeWantBook: %r>" % self.book.title

    def posted_to_string(self):
        return self.posted.strftime("%m/%d/%y")


class TradeHaveBook:
    id = db.Column(db.Integer, primary_key=True)
    book = db.Column(db.Integer, db.ForeignKey('book.id'))
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    posted = db.Column(db.DateTime, default=datetime.datetime.now)

    def __init__(self, book, user, posted):
        self.book = book
        self.user = user
        self.posted = posted

    def __repr__(self):
        return "<TradeWantHave: %r>" % self.book.title

    def posted_to_string(self):
        return self.posted.strftime("%m/%d/%y")
