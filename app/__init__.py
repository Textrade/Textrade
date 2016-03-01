from flask import Flask, render_template, g
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.mail import Mail
import flask_login

# Instantiate application
app = Flask(__name__)

# Takes configuration form config.py
app.config.from_object('config')

# Define database
db = SQLAlchemy(app)

#
# MAIL CONFIGURATION
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
# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'user.login'


@app.before_request
def before_request():
    g.user = flask_login.current_user
    g.domain = "http"


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
app.register_blueprint(user)

# Dashboard views
from app.dashboard.views import dashboard
app.register_blueprint(dashboard)

# Setup
# from app.user.models import UserRole
# db.create_all()
# db.drop_all()

# db.session.add(UserRole(role="customer"))
# db.session.add(UserRole(role="developer"))
# db.session.add(UserRole(role="admin"))
# db.session.commit()
