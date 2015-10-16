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
from user.forms import (RegisterForm, LoginForm, ResendToken,
                        ForgotCredentialReset, ResetPassword)
from user.user import create_user, get_user
from user.token import *

#
#
#   BOOK IMPORTS
#
#
from book.forms import (AddBookRentForm, AddBookTradeForm)
from book.book import (create_book_rent, allowed_file, load_book_info,
                       create_book_trade)

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
DEBUG = True
HOST = "127.0.0.1"
PORT = 5000

#
#
#
# MAIL CONFIG
#
#
#
mail = Mail()
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SENDER'] = "Textrade <umltextrade@gmail.com>"
app.config['MAIL_USERNAME'] = "umltextrade@gmail.com"
app.config['MAIL_PASSWORD'] = "Angell100."
mail.init_app(app)

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
        name="Book for Rent", model=models.BookRent, endpoint='book-rent', category="Book"
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
    g.db = models.db
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after every request."""
    g.db.close()
    return response


@app.errorhandler(404)
def page_not_page(e):
    return "The no found page!", 404


@app.errorhandler(500)
def internal_error(e):
    return "We have a internal error =(", 500


@app.route('/')
def index():
    return render_template('default/index.html')


@app.route('/team/')
def team():
    return render_template('misc/the-team.html')


@app.route('/login/', methods=('GET', 'POST'))
def login():
    # Login form in login view
    login_form = LoginForm()
    if not flask_login.current_user.is_authenticated():

        if login_form.validate_on_submit():
            username = login_form.username.data
            current_user = models.User.get(models.User.username == username)
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
            log_form=login_form
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
                personal_email=reg_form.personal_email.data
            )
            flash("User created successfully!", "success")
            token = generate_confirmation_token(reg_form.university_email.data)
            html = render_template('user/email_verification.html', token=token)
            subject = "Confirm email and activate your account!"
            send_email(
                to=reg_form.university_email.data,
                subject=subject,
                template=html
            )
            flash("An email confirmation has been sent to your email.", "success")
            return redirect(url_for('login'))
        return render_template('user/register.html', reg_form=reg_form, section="user", title="Register")
    flash("You are logged in.")
    return redirect(url_for('dashboard'))


@app.route('/user/activate/<token>/')
def confirm_email(token):
    try:
        email = confirm_token(token)
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
        flash("Your email have been confirmed.", "success")
    return redirect(url_for('dashboard'))


@app.route('/user/activate/resend/', methods=('GET', 'POST'))
def resend_token():
    form = ResendToken()
    if form.validate_on_submit():
        email = form.university_email.data
        token = generate_confirmation_token(email)
        html = render_template('user/email_verification.html', token=token)
        subject = "Confirm email and activate your account!"
        send_email(
            to=email,
            subject=subject,
            template=html
        )
        flash("The activation link have been resend!")
        return redirect(url_for('login'))
    return render_template('user/resend_token.html', form=form)


@app.route('/user/forgot/', methods=('POST', 'GET'))
def forgot_credentials():
    form = ForgotCredentialReset()
    if form.validate_on_submit():
        email = form.university_email.data
        token = generate_confirmation_token(email)
        html = render_template('user/reset_password_email.html', token=token)
        subject = "Reset password request"
        send_email(
            to=email,
            subject=subject,
            template=html
        )
        flash("We've sent you an email with a link to reset your password.")
        return redirect(url_for('login'))
    return render_template('user/forgot_credentials.html', form=form)


@app.route('/user/forgot/<token>/', methods=('POST', 'GET'))
def change_credentials(token):
    email = confirm_token(token)
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
        return render_template('user/reset_password.html', form=form)
    else:
        flash("The confirmation link is invalid or has expired.", "error")
        return redirect(url_for('forgot_credentials'))


@app.route('/user/<string:username>/')
def user_page(username):
    user = None
    try:
        user = models.User.get(models.User.username == username)
    except peewee.DoesNotExist:
        abort(404)
    user_rent_books = models.BookRent.select().where(models.BookRent.username == username)
    return render_template('user/user-page.html', user=user, rent_book=user_rent_books)


@app.route('/dashboard/')
@login_required
def dashboard():
    c_user = flask_login.current_user
    book_rent = models.BookRent.select().where(models.BookRent.username == c_user.username)
    return render_template('default/dashboard.html', c_user=c_user, book_for_rent=book_rent)


@app.route('/rent/')
def rent():
    return render_template('rent/rent.html')


@app.route('/book/add/', methods=('GET', 'POST'))
@login_required
def add_book():
    rent_book_form = AddBookRentForm()
    trade_book_form = AddBookTradeForm()

    if request.method == "POST":
        # Check which form was submitted
        which_form = request.form['hidden']
        if which_form is "0":
            # Add a book for rent
            if rent_book_form.validate_on_submit():
                # Get ISBN from form after validate
                isbn = rent_book_form.isbn.data
                # Try to load information
                book = load_book_info(isbn)
                if book:
                    file = request.files['img']
                    if file and allowed_file(file.filename, BOOK_IMG_EXTENTIONS):
                        # Secure the input file
                        filename = secure_filename(
                            "{}-{}.{}".format(
                                flask_login.current_user.username,
                                uuid.uuid4(),
                                file.filename.rsplit('.', 1)[1]
                            )
                        )
                        # Save the image to the server
                        img_path = DOMAIN_NAME + '/static/img/books/' + filename
                        file.save(os.path.join(UPLOAD_FOLDER, filename))
                        # Create a book record in the database
                        create_book_rent(
                            name=book['title'],
                            author=book['authors'],
                            description=book['description'],
                            isbn=isbn,
                            condition=rent_book_form.condition.data,
                            condition_comment=rent_book_form.condition_comment.data,
                            username=flask_login.current_user.username,
                            img_path=img_path
                        )
                        flash("You book have been created!", "success")
                        return redirect(url_for('add_book'))
                    else:
                        flash("This format of the file is not allowed.", "error")
                else:
                    flash("We couldn't find this book, check the ISBN number.", "error")
                    return redirect(url_for('add_book'))
        elif which_form is "1":
            # Add a book to trade
            if trade_book_form.validate_on_submit():
                have_book_isbn = trade_book_form.have_book.data
                want_book_isbn = trade_book_form.want_book.data
                create_book_trade(
                    want_isbn=want_book_isbn,
                    have_isbn=have_book_isbn,
                    user=flask_login.current_user.username
                )

    return render_template(
        'rent/rent-your-book.html',
        rent_form=rent_book_form,
        trade_form=trade_book_form
    )


@app.route('/rent/book/')
def rent_all_book():
    book = models.BookRent.select()
    return "All book for rent available..."


@app.route('/rent/book/search/')
def rent_search():
    return render_template('rent/rental-books-search.html')


@app.route('/rent/book/<string:username>/')
def rent_user_book(username):
    try:
        user = models.User.get(models.User.username == username)
    except peewee.DoesNotExist:
        abort(404)
    book_for_rent = models.User.select().where(models.BookRent.username == username)
    return "Book for rent for a particular user."


@app.route('/rent/book/<string:username>/<int:book_pk>/')
def rent_book(username, book_pk):
    try:
        user = get_user(username)
    except peewee.DoesNotExist:
        abort(404)

    user_books = models.BookRent.select().where(models.BookRent.username == username)

    try:
        book_ = models.BookRent.get(models.BookRent.id == book_pk)
    except peewee.DoesNotExist:
        abort(404)

    other_equal_books = models.BookRent.select().where(models.BookRent.isbn == book_.isbn)

    return render_template(
        'book/book-template.html',
        user=user,
        user_books=user_books,
        book=book_,
        other_equal_books=other_equal_books,
    )


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
