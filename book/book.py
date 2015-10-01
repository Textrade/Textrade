from flask_wtf import Form
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired, Regexp, ValidationError, Length
from models import BookRent


class AddBookForm(Form):
    passok
