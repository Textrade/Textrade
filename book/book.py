from flask_wtf import Form
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired, Regexp, ValidationError, Length
from models import Book


class AddBookForm(Form):
    passok
