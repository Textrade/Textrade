from flask_wtf import Form
from wtforms import (StringField, SelectField, FileField, TextAreaField,
                     BooleanField)
from wtforms.validators import DataRequired, Regexp, ValidationError, Length

from models import BookCondition


def check_file(ALLOWED_EXTENSIONS, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class AddBookRentForm(Form):
    """Form to add a book for rent"""
    book_title = StringField(
        'Book Title',
        validators=[
            DataRequired(),
        ]
    )
    isbn = StringField(
        'ISBN',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]+$',
                message="ISBN can only be numbers/"
            )
        ]
    )
    condition_list = [('', 'Select Condition')]
    for condition in BookCondition.select():
        condition_list.append((condition.condition, condition.condition))

    condition = SelectField(
        'Condition',
        choices=condition_list,
        validators=[
            DataRequired(),
        ]
    )
    condition_comment = TextAreaField()
    img = FileField(
        'Upload a picture'
    )
