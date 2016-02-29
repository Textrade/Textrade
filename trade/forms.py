from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp


class AddHaveBookTrade(Form):
    """Form to add a have book."""
    isbn = StringField(
        'Add a book by typing the ISBN',
        validators=[
            DataRequired()
        ]
    )


class AddWantBookTrade(Form):
    """Form to add a have book."""
    isbn = StringField(
        'Add a book by typing the ISBN',
        validators=[
            DataRequired()
        ]
    )
