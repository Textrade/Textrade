import requests
import json

from peewee import DoesNotExist

from models import BookRent, BookTradeWant, BookTradeHave, WishList


class DuplicateEntry(Exception):
    pass


class SelfBook(Exception):
    pass


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


def create_book_trade(**kwargs):
    """Crate a book to trade"""
    BookTradeWant.create(
        want_isbn=kwargs['want_isbn'],
        user=kwargs['user'],
    )
    BookTradeHave.create(
        have_isbn=kwargs['have_isbn'],
        user=kwargs['user']
    )


def load_book_info(isbn):
    """Get an ISBN and return a dictionary with book information."""
    data = requests.get("https://www.googleapis.com/books/v1/volumes?q={}".format(isbn)).json()
    if data['totalItems']:
        try:
            description = data['items'][0]['volumeInfo']['description']
        except KeyError:
            description = "No description available."
        book = {
            'title': data['items'][0]['volumeInfo']['title'],
            'authors': ', '.join(data['items'][0]['volumeInfo']['authors']),
            'description': description,
            'isbn': isbn,
        }
        return book
    return None


def get_book_rent(book_pk):
    return BookRent.get(BookRent.id == book_pk)


def add_to_wishlist(book_pk, username):
    """This function add a book to the wish if not duplicate."""
    try:
        wishlist = WishList.get((WishList.username == username) & (WishList.book == book_pk))
    except DoesNotExist:
        book = BookRent.get(BookRent.id == book_pk)
        if not book.username.username == username:
            WishList.create(
                book=book_pk,
                username=username,
            )
        else:
            raise SelfBook
    else:
        raise DuplicateEntry
