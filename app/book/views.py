from flask import Blueprint, redirect, url_for, jsonify

from app.book.forms import AddBookRentForm
from app.book.book import BookRentController
from app.core.google.google import GoogleAPI
from app.user.views import get_current_user


book = Blueprint('book', __name__)


@book.route('/book/add-book-to-rent', methods=['GET', 'POST'])
def add_book_rent():
    rent_book_form = AddBookRentForm()
    user = get_current_user()
    username = get_current_user().username  # If not accessed, undefined behavior occurs
    if rent_book_form.is_submitted():
        book_isbn = rent_book_form.isbn.data
        book = GoogleAPI.load_book_info(book_isbn)
        if book:
            BookRentController.create_renting_book(
                name=book['title'],
                author=book['authors'],
                description=book['description'],
                isbn=book_isbn,
                condition=rent_book_form.condition.data,
                condition_comment=rent_book_form.condition_comment.data,
                user=user,
                marks=rent_book_form.marks.data
            )
            return jsonify(
                status="success",
                msg="Your book have been added!",
                url=None
            )
        else:
            return jsonify(
                status="error",
                msg="We couldn't find this book, check the ISBN number",
                url=None
            )
    return redirect(url_for('dashboard.your_rentals'))
