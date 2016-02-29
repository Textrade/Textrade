from flask import (Blueprint, render_template, g, redirect,
                   url_for, request, flash)

init = Blueprint('init', __name__)


@init.route('/')
def index():
    from app.user.forms import RegisterForm
    return render_template("default/index.html",
                           register_form=RegisterForm())


@init.route('/search/')
def search():
    return render_template("rent/search.html")


@init.route('/services/')
def our_services():
    return render_template("misc/our-services.html")


@init.route('/team/')
def team():
    return render_template("misc/the-team.html")


@init.route('/faqs/')
def faqs():
    return render_template("misc/faqs.html")


@init.route('/contact/')
def contact():
    return render_template("misc/contact.html")


# This will be eliminated
@init.route('/send-email/')
def send_email():
    return render_template("email/send_email.html")


@init.route('/get_email_content/', methods=['GET', 'POST'])
def get_email_content():
    from app.tools.email import SendGridTest
    try:
        SendGridTest(
            request.form['email_content'],
            request.form['subject'],
            "Daniel Santos <{}>".format(request.form['from_email']),
            request.form['to_email'],
            request.form['cc_email']
        ).send()
        flash("Message send :)")
    except Exception as e:
        flash(e)

    return redirect(url_for('send_email'))
