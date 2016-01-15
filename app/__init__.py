from flask import (Flask, render_template, g)
from flask_sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
import flask_login

# Instantiate application
app = Flask(__name__)

# Takes configuration form config.py
app.config.from_object('config')

# Define database
db = SQLAlchemy(app)

#
# LOGIN MANAGER
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@app.before_request
def before_request():
    g.user = flask_login.current_user


# HTTP error handlers
@app.errorhandler(400)
def page_not_found(error):
    return render_template('misc/404.html')

# TODO: Add 500 server error handler


@app.route('/')
def index():
    return render_template("default/index.html")


@app.route('/search/')
def search():
    return render_template("rent/search.html")


@app.route('/services/')
def our_services():
    return render_template("misc/our-services.html")


@app.route('/team/')
def team():
    return render_template("misc/the-team.html")


@app.route('/faqs')
def faqs():
    return render_template("misc/faqs.html")


from app.user.views import user

app.register_blueprint(user)

db.create_all()
