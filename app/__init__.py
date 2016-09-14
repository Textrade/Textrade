from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import flask_login

import config

# Instantiate application
app = Flask(__name__)

# Takes configuration form config.py
app.config.from_object('config')

# Define database
db = SQLAlchemy(app)


# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


@app.before_request
def before_request():
    g.user = flask_login.current_user
    g.domain = config.DOMAIN_NAME


# HTTP error handlers
@app.errorhandler(400)
def page_not_found(error):
    return render_template('misc/404.html')

# TODO: Add 500 server error handler

# Default views
from app.views import init
app.register_blueprint(init)

# User views
from app.user.views import user
from app.user.models import UserRole
app.register_blueprint(user)

# Dashboard views
from app.dashboard.views import dashboard
app.register_blueprint(dashboard)


# Book views
from app.book.views import book
from app.book.models import (BookToRent, BookStatus, BookCondition,
                             BookTradeHave, BookTradeWant, BookRenting,
                             BookRentingRequest)
app.register_blueprint(book)

# config.init_project(app, db, reset=True)
