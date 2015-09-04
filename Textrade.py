from flask import (Flask, g, render_template, redirect, url_for, flash)

import models
from user.forms import RegisterForm
from user.user import create_user

app = Flask(__name__)


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


@app.route('/login')
def login_register():
    reg_form = RegisterForm()
    if reg_form.validate_on_submit():
        create_user(
            first_name=reg_form.first_name.data,
            last_name=reg_form.last_name.data,
            username=reg_form.username.data,
            password=reg_form.password.data,
            university_email=reg_form.university_email.data,
            personal_email=reg_form.personal_email.data
        )
        flash("User created successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('user/login.html', reg_form=reg_form)


@app.route('/register', methods=('GET', 'POST'))
def register():
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    return "Dashboard"


if __name__ == '__main__':
    app.run(debug=True)
