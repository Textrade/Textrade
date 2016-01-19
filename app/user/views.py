from flask import (Blueprint, request, render_template, flash,
                   g, session, redirect, url_for)
import flask_login
from flask_login import login_user, logout_user, login_required

from app.user.forms import (LoginForm, RegisterForm,
                            ResendActivationEmailForm, ForgotCredentialReset)
from app.user.user import UserController

user = Blueprint('user', __name__)


def get_current_user():
    return flask_login.current_user


@user.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if not get_current_user().is_authenticated():
        if login_form.validate_on_submit():
            try:
                current_user = UserController.get_user_by_username(login_form.username.data)
            except UserController.UserNotFound:
                flash("Your username  or password doesn't match!", "error")
                return redirect(url_for('user.login'))
            else:
                if current_user.is_active():
                    if UserController.check_hash(current_user.password, login_form.password.data):
                        login_user(current_user)  # Login/create session for the user
                        flash("You've been logged in!", "success")
                        next_page = request.args.get('next')
                        if next_page:
                            return redirect(next_page)
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
    # TODO: Find why this has been printing twice! If still doing
    flash("You are logged in already.", "success")
    return redirect(url_for('dashboard'))


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@user.route('/register/', methods=['GET', 'POST'])
def register():
    if not get_current_user().is_authenticated():
        reg_form = RegisterForm()
        if reg_form.validate_on_submit():
            university_email = reg_form.university_email.data
            try:
                new_user = UserController(
                    first_name=reg_form.first_name.data,
                    last_name=reg_form.last_name.data,
                    username=reg_form.username.data,
                    password=reg_form.password.data,
                    university_email=university_email
                ).create()
            except Exception:  # Don't know exactly the exception
                flash("We had a problem creating your user, please try again.")
                return redirect(url_for('login'))
            flash("User created successfully!", "success")

    return redirect(url_for('login'))


@user.route('/forgot-credentials')
def forgot_credentials():
    return "Forgot credentials"


@user.route('/resend-token')
def resend_token():
    return redirect(url_for('login'))
