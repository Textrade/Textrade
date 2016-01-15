from flask import (Blueprint, request, render_template, flash,
                   g, session, redirect, url_for)
import flask_login
from flask_login import login_user, logout_user, login_required

from app.user.forms import (LoginForm, RegisterForm,
                            ResendActivationEmailForm, ForgotCredentialReset)

user = Blueprint('user', __name__)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    # Login form in login view
    login_form = LoginForm()
    if not flask_login.current_user.is_authenticated():
        # if login_form.validate_on_submit():
        #     username = login_form.username.data
        #     try:
        #         current_user = models.User.get(models.User.username == username)
        #     except models.DoesNotExist:
        #         flash("Your username  or password doesn't match!", "error")
        #         return redirect(url_for('login'))
        #
        #     # TODO: Check this logic in the next try catch statement maybe no need it.
        #     if current_user.active:
        #         try:
        #             log_user = models.User.get(models.User.username == username)
        #         except models.DoesNotExist:
        #             flash("Your username  or password doesn't match!", "error")
        #         else:
        #             if check_password_hash(log_user.password, login_form.password.data):
        #                 login_user(log_user)
        #                 flash("You've been logged in!", "success")
        #                 _next = request.args.get('next')
        #                 if _next:
        #                     return redirect(_next)
        #                 else:
        #                     return redirect(url_for('dashboard'))
        #             else:
        #                 flash("Your username  or password doesn't match!", "error")
        #     else:
        #         flash("You account is not active yet, please check you email.", "no-active")
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


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@user.route('/register/')
def register():
    return redirect(url_for('login'))


@user.route('/forgot-credentials')
def forgot_credentials():
    return "Forgot credentials"


@user.route('/resend-token')
def resend_token():
    return redirect(url_for('login'))
