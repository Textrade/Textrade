from flask import (Blueprint, request, render_template, flash,
                   redirect, url_for, jsonify, abort)
import flask_login
from flask_login import login_user, logout_user, login_required
from itsdangerous import BadTimeSignature, SignatureExpired

import config
from app.user.forms import (LoginForm, RegisterForm,
                            ResendActivationEmailForm, ForgotCredentialReset)
from app.user.user import UserController
from app.book.book import BookRentController
from app import login_manager
from app.tools.email import EmailController, EmailException


user = Blueprint('user', __name__)


def get_current_user():
    return flask_login.current_user


@login_manager.user_loader
def load_user(userid):
    """Return a passed user.
    :param userid:
    """
    return UserController.get_user_by_id(userid)


@user.route('/login/', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if not get_current_user().is_authenticated():
        if login_form.is_submitted():
            try:
                current_user = UserController.get_user_by_username(login_form.username.data)
            except UserController.UserNotFound:
                return jsonify(
                    status="error",
                    msg="Your username  or password doesn't match!",
                    url=None
                )
            else:
                if UserController.check_hash(current_user.password, login_form.password.data):
                    if current_user.is_active():
                        try:
                            login_user(current_user)  # Login/create session for the user
                        except UserController.UserNotFound:
                            return jsonify(
                                status="error",
                                msg="We couldn't create a session for this user",
                                url=None
                            )
                        next_page = request.args.get('next')
                        if next_page:
                            return jsonify(
                                status="success",
                                msg="You've been logged in!",
                                url="{}{}".format(config.DOMAIN_NAME, url_for(next_page))
                            )
                        else:
                            return jsonify(
                                status="success",
                                msg=None,
                                url="{}{}".format(config.DOMAIN_NAME, url_for('dashboard.index'))
                            )
                    else:
                        return jsonify(
                            status="no-active",
                            msg="You account is not active yet, please check you email.",
                            url=None
                        )
                else:
                    return jsonify(
                        status="error",
                        msg="Your username  or password doesn't match!",
                        url=None
                    )
        return render_template(
            'user/login.html',
            section="user",
            title="Login",
            log_form=login_form,
            register_form=RegisterForm(),
            register_action="{}{}".format(config.DOMAIN_NAME, url_for('user.register')),
            user_check_api="{}{}".format(config.DOMAIN_NAME, url_for('user.check_username', username="{}")),
            forgot_form=ForgotCredentialReset(),
            resend_from=ResendActivationEmailForm()
        )
    return redirect(url_for('dashboard.index'))


@user.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("You've been successfully logged out.")
    return redirect(url_for('init.index'))


@user.route('/register/', methods=['GET', 'POST'])
def register():
    if not get_current_user().is_authenticated():
        reg_form = RegisterForm()
        if reg_form.is_submitted():
            university_email = reg_form.university_email.data
            new_user = UserController(
                first_name=reg_form.first_name.data,
                last_name=reg_form.last_name.data,
                username=reg_form.username.data,
                password=reg_form.password.data,
                university_email=university_email
            ).create()

            # TODO: Send email with SendGrid
            try:
                EmailController().send_activation_email(new_user)
            except EmailException:
                flash("We couldn't send you an activation email.", "resend-email")
                return jsonify(
                    status="no-active",
                    msg=("User created successfully! "
                         "We couldn't send you an activation email."),
                    url=None
                )
            return jsonify(
                status="success-no-active",
                msg=("User created successfully! "
                     "An email confirmation has been sent to your email."),
                url=None
            )
    return redirect(url_for('user.login'))


# TODO: Need to implement security or whole API
@user.route('/api/exist/<string:username>/')
def check_username(username):
    return jsonify(
        status=UserController.username_exists(username),
    )


@user.route('/confirm-email/<string:token>')
def confirm_email(token):
    try:
        UserController.activate_account(token)
    except SignatureExpired:
        flash("Your link has expired.", "resend-email")
    except BadTimeSignature:
        flash("Invalid activation link.", "resend-email")
    else:
        flash("Your user have been activated, please login!", "success")
    return redirect(url_for('user.login'))


@user.route('/resend-token/', methods=['GET', 'POST'])
def resend_token():
    resend_form = ResendActivationEmailForm()
    if resend_form.validate_on_submit():
        university_email = resend_form.university_email.data
        try:
            # TODO: Pass arguments to EmailController
            EmailController().send_activation_email(
                UserController.get_user_as_dict(university_email=university_email)
            )
        except UserController.UserNotFound as e:
            flash(str(e), "error")
            return redirect(url_for('user.login'))
        flash("We've resend an activation email to %s." % university_email, "success")
    return redirect(url_for('user.login'))


@user.route('/forgot-credentials/')
def forgot_credentials():
    return "Forgot credentials"


@user.route('/user/<string:username>')
def user_page(username):
    user_rv = None
    try:
        user_rv = UserController.get_user_by_username(username)
    except UserController.UserNotFound:
        abort(404)
    else:
        if not user_rv.is_active():
            abort(404)
    user_rent_books = BookRentController.get_available_rentals(username)
    return render_template('user/profile.html', user=user_rv, rent_book=user_rent_books)
