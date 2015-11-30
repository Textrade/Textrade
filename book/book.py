import requests
import json

from peewee import DoesNotExist

from models import (BookToRent, BookTradeWant, BookTradeHave, WishList, BookRentingRequest,
                    BookRenting)


class DuplicateEntry(Exception):
    pass


class SelfBook(Exception):
    pass


def allowed_file(filename, ALLOWED_EXTENSIONS):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_book_rent(**kwargs):
    """Create a book for rent."""
    BookToRent.create(
        name=kwargs['name'],
        author=kwargs['author'],
        description=kwargs['description'],
        isbn=kwargs['isbn'],
        condition=kwargs['condition'],
        condition_comment=kwargs['condition_comment'],
        marks=kwargs['marks'],
        username=kwargs['username'],
        available='available',
        # image_path=kwargs['img_path']
    )


def request_book_rent(book_id, username):
    """This function request a book to be rented."""
    BookRentingRequest.create(
        book=book_id,
        rentee=username,
    )


def accept_request_to_rent(request_id):
    """This function accept a request to rent."""
    request = BookRentingRequest.get(BookRentingRequest.id == request_id)
    book = BookToRent.get(BookToRent.id == request.book)

    BookRenting.create(
        book=book.id,
        renter=book.username.username,
        rentee=request.rentee.username
    )

    request.delete_instance()


def delete_book_rent(book_id):
    """This function delete a book for rent."""
    BookToRent.get(BookToRent.id == book_id).delete_instance()


def create_book_trade(**kwargs):
    """Crate a book to trade"""
    BookTradeWant.create(
        name=kwargs['want_name'],
        isbn=kwargs['want_isbn'],
        user=kwargs['user'],
    )
    BookTradeHave.create(
        name=kwargs['have_name'],
        isbn=kwargs['have_isbn'],
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
    return BookToRent.get(BookToRent.id == book_pk)


def add_to_wishlist(book_pk, username):
    """This function add a book to the wish if not duplicate."""
    try:
        wishlist = WishList.get((WishList.username == username) & (WishList.book == book_pk))
    except DoesNotExist:
        book = BookToRent.get(BookToRent.id == book_pk)
        if not book.username.username == username:
            WishList.create(
                book=book_pk,
                username=username,
            )
        else:
            raise SelfBook
    else:
        raise DuplicateEntry
