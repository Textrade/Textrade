from flask_wtf import Form
from wtforms import StringField, FieldList
from wtforms.validators import DataRequired, Regexp, ValidationError, Length
from models import BookRent


def check_file(ALLOWED_EXTENSIONS, filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


class AddBookForm(Form):
    pass
