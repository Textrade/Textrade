from flask_wtf import Form
from wtforms import (StringField, SelectField, FileField, TextAreaField,
                     BooleanField)
from wtforms.validators import DataRequired, Regexp, ValidationError, Length

from app.book.models import BookCondition


def check_file(ALLOWED_EXTENSIONS, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class AddBookRentForm(Form):
    """Form to add a book for rent"""
    book = StringField(
        'Book Title (Edition)',
        validators=[
            DataRequired(),
        ]
    )
    isbn = StringField(
        'ISBN',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9-]+$',
                message="ISBN can only be numbers"
            )
        ]
    )
    condition_list = []
    for condition in BookCondition.query.all():
        condition_list.append((condition.condition, condition.label))

    condition = SelectField(
        'Condition',
        choices=condition_list,
        validators=[
            DataRequired(message="Please let us know what is the condition"),
        ]
    )
    condition_comment = TextAreaField('Book condition comments (if any)')
    marks = BooleanField('Are there markings inside the book? (Notes in margins etc.?)')
    # img = FileField(
    #     'Upload a picture',
    #     validators=[
    #         DataRequired(message="Please provide a picture, people want to see your book.")
    #     ]
    # )


class AddBookTradeForm(Form):
    """BookTradeForm"""
    want_book = StringField(
        'ISBN',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9a-zA-Z-]+$',
                message="ISBN can only be numbers"
            )
        ]
    )
    have_book = StringField(
        'ISBN',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9a-zA-Z-]+$',
                message="ISBN can only be numbers"
            )
        ]
    )
