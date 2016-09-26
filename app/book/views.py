from flask import Blueprint, redirect, url_for, jsonify
from flask_login import login_required

from app.book.models import BookToRent
from app.book.forms import AddBookRentForm
from app.book.book import BookRentController
from app.core.google.google import GoogleAPI
from app.user.views import get_current_user


book = Blueprint('book', __name__)


@book.route('/book/rent/add', methods=['GET', 'POST'])
@login_required
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


@book.route('/book/rent/delete/<int:pk>', methods=['GET'])
@login_required
def delete_book_rent(pk):
    user = get_current_user()
    book_rent = BookToRent.get_by_id(pk)

    if book_rent:
        if user.id == book_rent.user_id:
            BookRentController.delete_book_to_rent(pk)
            return jsonify(
                status="success",
                msg="Your book was delete successfully",
                url=None
            )
        else:
            return jsonify(
                status="error",
                msg="You are trying to delete a book that is not yours, this will be reported",
                url=None
            )
    else:
        return jsonify(
            status="error",
            msg="The book that you are try to delete doesn't exists",
            url=None
        )
