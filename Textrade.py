# # # # # # # # # # # # # # # # # # # # # # # # # # #
#                                                   #
#   PROJECT: Textrade                               #
#   CONTRIBUTORS:   Daniel Santos (Back-End),       #
#                   Nina Petropoulos (Front-End)     #
#   VERSION: 1.0                                    #
#                                                   #
# # # # # # # # # # # # # # # # # # # # # # # # # # #

#
#
#   PYTHON IMPORTS
#
#
import datetime
import os

#
#
#
#   FLASK IMPORTS
#
from flask import (Flask, g, render_template, redirect, url_for,
                   flash, request, abort)
from flask.ext.bcrypt import check_password_hash, generate_password_hash
from flask.ext.mail import Mail
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required)
import flask_wtf
import flask_login

#
#
#
#   TOOLS IMPORTS
#
#
from werkzeug.utils import secure_filename
import uuid
import peewee

#
#
#   ADMIN IMPORTS
#
#
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

#
#
#   MODELS IMPORTS
#
#
import models

#
#
#   USER IMPORTS
#
#
from user.forms import (RegisterForm, LoginForm, ResendActivationEmailForm,
                        ForgotCredentialReset, ResetPassword)
from user.user import create_user, get_user, get_rentals
from user.token import *

#
#
#   BOOK IMPORTS
#
#
from book.forms import (AddBookRentForm, AddBookTradeForm)
from book.book import *

#
#
#
# APP CONFIG
#
#
#
app = Flask(__name__)
app.secret_key = '&#*A_==}{}#QPpa";.=1{@'
app.config['SECURITY_PASSWORD_SALT'] = '(text)rade*'
app.config['CSRF_ENABLED'] = True
DEBUG = False
HOST = "127.0.0.1"
PORT = 5000

#
#
#
# MAIL CONFIG
#
#
#
MAIL = Mail()
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SENDER'] = "Textrade <umltextrade@gmail.com>"
app.config['MAIL_USERNAME'] = "umltextrade@gmail.com"
app.config['MAIL_PASSWORD'] = "Angell100."
MAIL.init_app(app)

#
#
#
# LOGIN MANAGER CONFIG
#
#
#
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#
#
#
# UPLOAD MANAGER CONFIG
#
#
#
DOMAIN_NAME = "http://127.0.0.1:5000"
UPLOAD_FOLDER = '/Users/dsantos/Web Projects/Textrade/Textrade/static/img/books/'
BOOK_IMG_EXTENTIONS = {'jpg', 'png', 'jpeg'}

#
#
#
# GOOGLE'S API CONFIG
#
#
#
BOOK_API_KEY = "AIzaSyBI_bJjoReQ2WboaqJvA6wA6lDraR9sJ54"


#
#
#
# FLASK ADMIN CONFIG
#
#
#
class TextradeModelView(ModelView):
    """ModelView override."""
    form_base_class = flask_wtf.Form
    # Exclude encrypted password from admin view
    column_exclude_list = [
        'password', 'description', 'image_path'
    ]
    form_excluded_columns = ['password', ]
    column_details_exclude_list = ['password', ]

    def is_accessible(self):
        return flask_login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

admin = Admin(app, name="Textrade", template_mode="bootstrap3")

#
#   USERS
#
admin.add_view(
    TextradeModelView(
        name="Users", model=models.User, endpoint="users", category="User"
    )
)
admin.add_view(
    TextradeModelView(
        name="User Role", model=models.UserRole, endpoint="user-role", category="User"
    )
)

#
#   TRADES
#
admin.add_view(
    TextradeModelView(
        name="Trades", model=models.Trade, endpoint="trades", category="Trade",
    )
)
admin.add_view(
    TextradeModelView(
        name="Trade Status", model=models.TradeStatus, endpoint="trade-status", category="Trade"
    )
)

#
#   BOOKS
#
admin.add_view(
    TextradeModelView(
        name="Book for Rent", model=models.BookToRent, endpoint='book-rent', category="Book"
    )
)
admin.add_view(
    TextradeModelView(
        name="Book to Trade Wanted", model=models.BookTradeWant, endpoint="book-trade-wanted", category="Book"
    )
)
admin.add_view(
    TextradeModelView(
        name="Book to Trade Have", model=models.BookTradeHave, endpoint="book-trade-have", category="Book"
    )
)
admin.add_view(
    TextradeModelView(
        name="Book Status", model=models.BookStatus, endpoint="book-status", category="Book"
    )
)
admin.add_view(
    TextradeModelView(
        name="Book Condition", model=models.BookCondition, endpoint="book-condition", category="Book"
    )
)


def get_current_user():
    return flask_login.current_user


@login_manager.user_loader
def load_user(userid):
    """Return a passed user."""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    """Connect to the database before a request."""
    g.user = get_current_user()
    g.domain = "https://textrade.herokuapp.com"
    g.db = models.db
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after every request."""
    g.db.close()
    return response


@app.errorhandler(404)
def page_not_page(e):
    return render_template('misc/404.html'), 404


@app.errorhandler(500)
def internal_error(e):
    return "We have a internal error =(", e


@app.route('/')
def index():
    return render_template(
        'default/index.html',
        register_form=RegisterForm()
    )


@app.route('/team/')
def team():
    return render_template('misc/the-team.html')


@app.route('/contact-us/')
@app.route('/contact/')
def contact():
    return render_template('misc/contact.html')


@app.route('/our-services/')
@app.route('/services/')
def our_services():
    return render_template('misc/our-services.html')


@app.route('/faqs/')
def faqs():
    return render_template('misc/faqs.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    # Login form in login view
    login_form = LoginForm()
    if not flask_login.current_user.is_authenticated():

        if login_form.validate_on_submit():
            username = login_form.username.data
            try:
                current_user = models.User.get(models.User.username == username)
            except models.DoesNotExist:
                flash("Your username  or password doesn't match!", "error")
                return redirect(url_for('login'))

            # TODO: Check this logic in the next try catch statement maybe no need it.
            if current_user.active:
                try:
                    log_user = models.User.get(models.User.username == username)
                except models.DoesNotExist:
                    flash("Your username  or password doesn't match!", "error")
                else:
                    if check_password_hash(log_user.password, login_form.password.data):
                        login_user(log_user)
                        flash("You've been logged in!", "success")
                        _next = request.args.get('next')
                        if _next:
                            return redirect(_next)
                        else:
                            return redirect(url_for('dashboard'))
                    else:
                        flash("Your username  or password doesn't match!", "error")
            else:
                flash("You account is not active yet, please check you email.", "no-active")
        return render_template(
            'user/login.html',
            section="user",
            title="Login",
            log_form=login_form,
            register_form=RegisterForm(),
            forgot_form=ForgotCredentialReset(),
            resend_from=ResendActivationEmailForm()
        )
    # TODO: Find why this has been printing twice!
    flash("You are logged in already.", "success")
    return redirect(url_for('dashboard'))


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out.")
    return redirect(url_for('index'))


@app.route('/register/', methods=('GET', 'POST'))
def register():
    # Registration form in login view
    if not flask_login.current_user.is_authenticated():
        reg_form = RegisterForm()
        if reg_form.validate_on_submit():
            create_user(
                first_name=reg_form.first_name.data,
                last_name=reg_form.last_name.data,
                username=reg_form.username.data,
                password=generate_password_hash(reg_form.password.data),
                university_email=reg_form.university_email.data,
            )
            flash("User created successfully!", "success")
            token = generate_confirmation_token(reg_form.university_email.data, secret_key=app.secret_key)
            html = render_template(
                'email/verifyNewAccount/verification.html',
                token=token,
                name=reg_form.first_name.data,

            )
            subject = "Confirm email and activate your account!"

            msg = Message(
                subject,
                recipients=[reg_form.university_email.data],
                html=html,
                sender=app.config['MAIL_SENDER']
            )
            MAIL.send(msg)

            flash("An email confirmation has been sent to your email.", "success")
            return redirect(url_for('login'))
        for errors in reg_form.errors.items():
            for error in errors[1]:
                flash("{}".format(error))
        return redirect(url_for('login'))
    flash("You are logged in.")
    return redirect(url_for('dashboard'))


@app.route('/user/activate/<string:token>/')
def confirm_email(token):
    try:
        email = confirm_token(token, app.config['SECRET_KEY'])
    except BadSignature:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for('index'))
    user = models.User.get(models.User.university_email == email)
    if user.active:
        flash("You email is already confirmed. Please login.", "success")
        return redirect(url_for('login'))
    else:
        user.update(
            active=True,
            activated_on=datetime.datetime.now()
        ).execute()
        html = render_template(
            'email/confirmation/confirmation.html',
            name=user.first_name,
            # One means it activation
            centi=1
        )
        subject = "You account is active!"

        msg = Message(
            subject,
            recipients=[user.university_email],
            html=html,
            sender=app.config['MAIL_SENDER']
        )
        MAIL.send(msg)

        flash("Your email have been confirmed.", "success")
    return redirect(url_for('dashboard'))


@app.route('/user/activate/resend/', methods=('GET', 'POST'))
def resend_token():
    form = ResendActivationEmailForm()
    if form.validate_on_submit():
        email = form.university_email.data
        try:
            user = models.User.get(models.User.university_email == email)
        except models.DoesNotExist:
            flash("This email is not in our system")
            return redirect(url_for('login'))
        token = generate_confirmation_token(email, app.config['SECRET_KEY'])
        html = render_template(
            'email/verifyNewAccount/verification.html',
            token=token,
            name=user.first_name
        )
        subject = "Confirm email and activate your account!"

        msg = Message(
            subject,
            recipients=[email],
            html=html,
            sender=app.config['MAIL_SENDER']
        )
        MAIL.send(msg)

        flash("The activation link have been resend!")
        return redirect(url_for('login'))
    for errors in form.errors.items():
        for error in errors[1]:
            flash("{}".format(error))
    return redirect(url_for('login'))


@app.route('/user/forgot/', methods=('POST', 'GET'))
def forgot_credentials():
    form = ForgotCredentialReset()
    if form.validate_on_submit():
        email = form.university_email.data
        try:
            user = models.User.get(models.User.university_email == email)
        except models.DoesNotExist:
            flash("This email is not in our system")
            return redirect(url_for('login'))
        token = generate_confirmation_token(email, app.secret_key)
        html = render_template(
            'email/forgotPassword/forgotPassword.html',
            token=token,
            name=user.first_name
        )
        subject = "Reset password request"

        msg = Message(
            subject,
            recipients=[email],
            html=html,
            sender=app.config['MAIL_SENDER']
        )
        MAIL.send(msg)

        flash("We've sent you an email with a link to reset your password.")
        return redirect(url_for('login'))
    for errors in form.errors.items():
        for error in errors:
            flash("{}".format(error))
    return redirect(url_for('login'))


@app.route('/user/forgot/<string:token>/', methods=('POST', 'GET'))
def change_credentials(token):
    email = confirm_token(token, app.secret_key)
    if email:
        try:
            user = models.User.get(models.User.university_email == email)
        except models.DoesNotExist:
            flash("Something went wrong with your username.")
            return redirect(url_for('login'))
        form = ResetPassword()
        if form.validate_on_submit():
            user.update(
                password=generate_password_hash(form.password.data)
            ).execute()
            flash("Your password was reset successfully")
            return redirect(url_for('login'))
        # TODO: Need a page to change the password
        return render_template('user/reset_password.html', form=form)
    else:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for('login'))


@app.route('/user/<string:username>/')
def user_page(username):
    user = None
    try:
        user = models.User.get(models.User.username == username)
    except peewee.DoesNotExist:
        abort(404)
    user_rent_books = models.BookToRent.select().where(models.BookToRent.username == username)
    return render_template('user/profile.html', user=user, rent_book=user_rent_books)


@app.route('/rent/')
def rent():
    return render_template('rent/rent.html')


@app.route('/rent/book/')
def rent_all_book():
    book = models.BookToRent.select()
    return "All book for rent available..."


@app.route('/book/add/', methods=('GET', 'POST'))
@login_required
def add_book_rent():
    rent_book_form = AddBookRentForm()
    # Add a book for rent
    if rent_book_form.validate_on_submit():
        # Get ISBN from form after validate
        isbn = rent_book_form.isbn.data
        # Try to load information
        book = load_book_info(isbn)
        if book:
            # file = request.files['img']
            # if file and allowed_file(file.filename, BOOK_IMG_EXTENTIONS):
            #     # Secure the input file
            #     filename = secure_filename(
            #         "{}-{}.{}".format(
            #             flask_login.current_user.username,
            #             uuid.uuid4(),
            #             file.filename.rsplit('.', 1)[1]
            #         )
            #     )
            #     # Save the image to the server
            #     img_path = DOMAIN_NAME + '/static/img/books/' + filename
            #     file.save(os.path.join(UPLOAD_FOLDER, filename))
                # Create a book record in the database
            create_book_rent(
                name=book['title'],
                author=book['authors'],
                description=book['description'],
                isbn=isbn,
                condition=rent_book_form.condition.data,
                condition_comment=rent_book_form.condition_comment.data,
                username=get_current_user().username,
                marks=rent_book_form.marks.data,
                # img_path=img_path
            )
            flash("You book have been created!", "success")
            return redirect(url_for('add_book_rent'))
            # else:
            #     flash("This format of the file is not allowed.", "error")
        else:
            flash("We couldn't find this book, check the ISBN number.", "error")
            return redirect(url_for('add_book_rent'))

    for errors in rent_book_form.errors.items():
        for error in errors[1]:
            flash("{}".format(error))
    return redirect(url_for('your_rentals'))


@app.route('/rent/book/<string:username>/')
def rent_user_book(username):
    try:
        user = models.User.get(models.User.username == username)
    except peewee.DoesNotExist:
        abort(404)
    book_for_rent = models.User.select().where(models.BookToRent.username == username)
    return "Book for rent for a particular user."


@app.route('/rent/book/<int:book_pk>/')
def book_page(book_pk):
    try:
        user = get_user(book_pk)
    except peewee.DoesNotExist:
        abort(404)

    user_books = models.BookToRent.select().where(models.BookToRent.username == user.username)

    try:
        book_ = models.BookToRent.get(models.BookToRent.id == book_pk)
    except peewee.DoesNotExist:
        abort(404)

    other_equal_books = models.BookToRent.select().where(models.BookToRent.isbn == book_.isbn)

    return render_template(
        'book/book.html',
        user=user,
        user_books=user_books,
        book=book_,
        other_equal_books=other_equal_books,
        joined=user.joined_to_string()
    )


@app.route('/rent/book/delete/<int:book_pk>')
@login_required
def delete_book(book_pk):
    book_owner = get_user(book_pk)
    # Check if the user logged in match the book onwer.
    if book_owner.username == get_current_user():
        try:
            models.BookToRent.get(BookToRent.id == book_pk).delete_instance()
        except models.DoesNotExist:
            flash("This book doesn't exists.")
        flash("The book have been deleted.")
        return redirect(url_for('dashboard'))
    flash("You are not the owner of this book.", "error")
    return redirect(url_for('book_page', book_pk=book_pk))


@app.route('/rent/book/wishlist/add/<int:book_pk>/')
@login_required
def wishlist_add(book_pk):
    c_user = flask_login.current_user.username
    try:
        add_to_wishlist(book_pk, c_user)
    except peewee.DoesNotExist:
        abort(404)
    except DuplicateEntry:
        flash("This book is already in your wishlist!", "error")
        return redirect(url_for('book_page', username=c_user, book_pk=book_pk))
    except SelfBook:
        flash("This is your own book, you can't add it", "error")
        return redirect(url_for('book_page', username=c_user, book_pk=book_pk))
    flash("Book added to your wishlist!", "success")
    return redirect(url_for('book_page', username=c_user, book_pk=book_pk))


@app.route('/search/')
@login_required
def search():
    return render_template(
        'rent/search.html',
        rentals=models.BookToRent.select().where(
            ~(models.BookToRent.username == get_current_user().username)
        )
    )

#
#   DASHBOARD
#


@app.route('/dashboard/')
@login_required
def dashboard():
    book_rent = models.BookToRent.select().where(models.BookToRent.username == get_current_user())
    wanted_books = models.BookTradeWant.select().where(models.BookTradeWant.user == get_current_user())
    have_books = models.BookTradeHave.select().where(models.BookTradeHave.user == get_current_user())
    return render_template(
        'dashboard/index.html',
        title="Dashboard",
        book_for_rent=book_rent,
        w_books=wanted_books,
        h_books=have_books,
    )


@app.route('/dashboard/your-rentals/')
@app.route('/dashboard/rentals/')
@login_required
def your_rentals():
    user = get_current_user()
    return render_template(
        'dashboard/rentals.html',
        title="Your Rentals",
        rental_list=get_rentals(
            user
        ),
        add_rental_form=AddBookRentForm(),
        currently_renting=get_currently_renting(user.username),
        currently_renting_out=get_currently_renting_out(user.username)
    )


@app.route('/dashboard/rentals/delete/<int:book_id>')
@login_required
def delete_rental_book(book_id):
    username = models.BookToRent.get(BookToRent.id == book_id).username.username
    if get_current_user().username == username:
        try:
            delete_book_rent(book_id)
        except models.DoesNotExist:
            flash("The book that you are try to delete doesn't exists.", "error")
        flash("Your book was delete successfully.", "success")
    else:
        flash("You are trying to delete a book that is not yours, this will be reported.", "error")
        # TODO: Report this to log.
    return redirect(url_for('your_rentals'))


@app.route('/dashboard/rentals-requests/')
@login_required
def rental_requests():
    user = get_current_user()
    return render_template(
        'dashboard/rental-requests.html',
        title="Rental Requests",
        incoming_rentals=get_user_renting_incoming_requests(user.username),
        outgoing_rentals=get_user_renting_outgoing_request(user.username)
    )


@app.route('/dashboard/rentals-requests/request-book/<int:book_id>/',)
@login_required
def request_book(book_id):
    try:
        status = models.BookToRent.get(BookToRent.id == book_id).is_available()
    except models.DoesNotExist:
        flash("The book that you are trying to request doesn't exists", "error")
        return redirect(url_for('rental_requests'))
    else:
        try:
            models.BookRentingRequest.get(
                (models.BookRentingRequest.book == book_id) &
                (models.BookRentingRequest.rentee == get_current_user().username)
            )
        except models.DoesNotExist:
            if status:
                create_request_book_rent(book_id=book_id, username=get_current_user().username)
                flash("This book have been requested!", "success")
                # TODO: Send email confirmation
                return redirect(url_for('rental_requests'))
            else:
                flash("The book that you are trying to request is not available at this time", "error")
                return redirect(url_for('rental_requests'))
        else:
            flash("You have requested this book already", "error")
            return redirect(url_for('rental_requests'))


@app.route('/dashboard/rentals-requests/accept-requests/<int:request_id>/')
@login_required
def accept_rental_request(request_id):
    try:
        book_request = models.BookRentingRequest.get(
            models.BookRentingRequest.id == request_id
        )
    except models.DoesNotExist:
        flash("This request doesn't exists", "error")
        return redirect(url_for('rental_requests'))
    else:
        book = models.BookToRent.get(
            models.BookToRent.id == book_request.book
        )
        renter = book.username

        if get_current_user().username == renter.username:
            accept_request_to_rent(request_id)
            flash(
                "You have accepted this requests, you will get an email with instruction on how to proceed",
                "success"
            )
            return redirect(url_for('rental_requests'))
        else:
            flash("You are not the owner of this book.")
            return redirect(url_for('rental_requests'))


@app.route('/dashboard/rentals-requests/delete-request/<int:request_id>/')
@login_required
def delete_rental_request(request_id):
    try:
        delete_request_book_rent(request_id, get_current_user().username)
    except models.DoesNotExist:
        flash("This request doesn't exists", "error")
        return redirect(url_for('rental_requests'))
    flash("The request was deleted successfully", "success")
    return redirect(url_for('rental_requests'))


@app.route('/dashboard/trades/')
@login_required
def trades():
    return render_template(
        'dashboard/trades.html',
        title="Trades",
    )


@app.route('/dashboard/trade-requests/')
@login_required
def trade_requests():
    return render_template(
        'dashboard/trade-requests.html',
        title="Trade Requests"
    )


@app.route('/dashboard/setting/')
@login_required
def account_settings():
    return render_template(
        'dashboard/account-settings.html',
        title="Account Settings"
    )


@app.route('/dashboard/history/')
@login_required
def account_history():
    return render_template(
        'dashboard/history.html',
        title="History"
    )


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
