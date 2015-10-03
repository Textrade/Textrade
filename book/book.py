import requests
import json

from models import BookRent


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_book_rent(**kwargs):
    """Create a book for rent."""
    BookRent.create(
        name=kwargs['name'],
        author=kwargs['author'],
        description=kwargs['description'],
        isbn=kwargs['isbn'],
        condition=kwargs['condition'],
        condition_comment=kwargs['condition_comment'],
        username=kwargs['username'],
        available='available',
        image_path=kwargs['img_path']
    )


def load_book_info(isbn):
    """Get an ISBN and return a dictionary with book information."""
    data = requests.get("https://www.googleapis.com/books/v1/volumes?q={}".format(isbn)).json()
    if data['totalItems']:
        book = {
            'title': data['items'][0]['volumeInfo']['title'],
            'authors': ', '.join(data['items'][0]['volumeInfo']['authors']),
            'description': data['items'][0]['volumeInfo']['description'],
            'isbn': isbn,
        }
        return book
    return None
