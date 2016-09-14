from .models import BookToRent, BookRenting, BookRentingRequest
from app.user.models import User


class BookRentController:
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
            book_status=1,
        ).create()
        return book

    @staticmethod
    def create_renting_request(book_id, user):
        book = BookRentController.get_book_to_rent(book_id)
        if book:
            return BookRentingRequest(
                book,
                book.user,
                user
            ).create()
        return None

    @staticmethod
    def delete_renting_request(pk):
        BookRentingRequest.query.filter_by(id=pk).delete()

    @staticmethod
    def accept_renting_request(request_id):
        renting_request = BookRentingRequest.query.filter_by(
            id=request_id).first()
        return BookRenting.create_from_request(renting_request)

    @staticmethod
    def get_currently_renting(user_id):
        return BookRenting.query.filter_by(rentee_id=user_id)

    @staticmethod
    def get_currently_renting_out(user_id):
        return BookRenting.query.filter_by(renter_id=user_id)

    @staticmethod
    def get_renting_request_by_id(request_id):
        return BookRentingRequest.query.filter_by(id=request_id).first()

    @staticmethod
    def get_user_renting_incoming_requests(user_id):
        return BookRentingRequest.query.filter_by(renter_id=user_id)

    @staticmethod
    def get_user_renting_outgoing_request(user_id):
        return BookRentingRequest.query.filter_by(rentee_id=user_id)

    @staticmethod
    def get_book_to_rent(book_id):
        return BookToRent.query.filter_by(id=book_id).first()

    @staticmethod
    def get_available_rentals(username):
        return BookToRent.query.filter_by(
            user_id=User.get_by_username(username).id
        )

    @staticmethod
    def get_book_to_rent_user(book_id):
        return BookRentController.get_book_to_rent(book_id).user

    @staticmethod
    def delete_book_to_rent(book_id):
        BookToRent.query.filter_by(id=book_id).delete()

    class DuplicateEntry(Exception):
        pass

    class SelfBook(Exception):
        pass
