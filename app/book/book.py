import requests
import json

from app import db
from .models import (BookToRent, BookTradeWant, BookTradeHave, BookRenting,
                     BookRentingRequest)


class BookController:

    @staticmethod
    def allowed_file(filename, allowed_extensions):
        return '.' in filename \
               and filename.rsplit('.', 1)[1] in allowed_extensions

    @staticmethod
    def create_renting_book(**kwargs):
        book = BookToRent(
            name=kwargs['name'],
            author=kwargs['author'],
            description=kwargs['description'],
            isbn=kwargs['isbn'],
            condition=kwargs['condition'],
            comment=kwargs['condition_comment'],
            marks=kwargs['marks'],
            user=kwargs['user'],
            book_status='available',
        ).create()
        return book

    @staticmethod
    def create_renting_request(book_id, user):
        book = BookController.get_book_to_rent(book_id)
        if book:
            return BookRentingRequest(
                book,
                book.user,
                user
            ).create()
        return None

    @staticmethod
    def delete_renting_request(pk):
        pass

    @staticmethod
    def accept_renting_request(request_id):
        pass

    @staticmethod
    def get_currently_renting(username):
        pass

    @staticmethod
    def get_currently_renting_out(username):
        pass

    @staticmethod
    def get_book_to_rent(book_id):
        return BookToRent.query.filter_by(id=book_id).first()

    @staticmethod
    def get_book_to_rent_user(book_id):
        return BookController.get_book_to_rent(book_id).user

    class DuplicateEntry(Exception):
        pass

    class SelfBook(Exception):
        pass
