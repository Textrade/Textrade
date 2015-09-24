import datetime

from itsdangerous import URLSafeSerializer, BadSignature
from flask import (Flask, g, render_template, redirect, url_for, flash, request)
from flask.ext.bcrypt import check_password_hash, generate_password_hash
from flask.ext.mail import Mail, Message
from flask.ext.login import (LoginManager, login_user, logout_user,
                             login_required)
import flask_wtf
import flask_login
from flask_admin import Admin
from flask_admin.contrib.peewee import ModelView

import models
from user.forms import RegisterForm, LoginForm, ResendToken
from user.user import create_user
from user.token import *


# DATABASE CONFIG
DEBUG = True
HOST = "127.0.0.1"
PORT = 5000

# APP CONFIG
app = Flask(__name__)
app.secret_key = '&#*A_==}{}#QPpa";.=1{@'
app.config['SECURITY_PASSWORD_SALT'] = '(text)rade*'
app.config['CSRF_ENABLED'] = True

# MAIL CONFIG
mail = Mail()
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_SENDER'] = "Textrade <umltextrade@gmail.com>"
app.config['MAIL_USERNAME'] = "umltextrade@gmail.com"
app.config['MAIL_PASSWORD'] = "Angell100."
mail.init_app(app)

# LOGIN MANAGER CONFIG
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class TextradeModelView(ModelView):
    """ModelView override."""
    form_base_class = flask_wtf.Form
    # Exclude encrypted password from admin view
    column_exclude_list = ['password', ]
    form_excluded_columns = ['password', ]
    column_details_exclude_list = ['password', ]

    def is_accessible(self):
        return flask_login.current_user.is_authenticated()

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('login', next=request.url))

admin = Admin(app, name="Textrade", template_mode="bootstrap3")
admin.add_view(TextradeModelView(models.UserRole))
admin.add_view(TextradeModelView(models.User))
admin.add_view(TextradeModelView(models.TradeStatus))
admin.add_view(TextradeModelView(models.Trade))
admin.add_view(TextradeModelView(models.BookStatus))
admin.add_view(TextradeModelView(models.Book))


@login_manager.user_loader
def load_user(userid):
    """Return a passed user."""
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out.")
    return redirect(url_for('index'))


@app.before_request
def before_request():
    """Connect to the database before a request."""
    g.db = models.db
    g.db.connect()


@app.after_request
def after_request(response):
    """Close the database connection after everything request."""
    g.db.close()
    return response


@app.route('/')
def index():
    return render_template('default/index.html')


@app.route('/team')
def team():
    return render_template('misc/the-team.html')


@app.route('/login', methods=('GET', 'POST'))
def login():
    # Login form in login view
    login_form = LoginForm()
    if not flask_login.current_user.is_authenticated():
        if login_form.validate_on_submit():
            try:
                log_user = models.User.get(models.User.username == login_form.username.data)
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
        return render_template(
            'user/login.html',
            section="user",
            title="Login",
            log_form=login_form
        )
    # TODO: Find why this has been printing twice!
    flash("You are logged in already.", "success")
    return redirect(url_for('dashboard'))


@app.route('/register', methods=('GET', 'POST'))
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


@app.route('/user/activate/<token>')
@login_required
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


@app.route('/user/activate/resend', methods=('GET', 'POST'))
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
        return redirect(url_for('index'))
    return render_template('user/resend_token.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    c_user = flask_login.current_user
    return render_template('default/dashboard.html', c_user=c_user)


@app.route('/rent')
def rent():
    return render_template('rent/rent.html')


@app.route('/rent/your-book')
def rent_your_book():
    return render_template('rent/rent-your-book.html')


@app.route('/rent/search')
def rent_search():
    return render_template('rent/rent-books-search.html')


if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
