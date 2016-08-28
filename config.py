import os

# Debug environment variable
DEBUG = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Runtime Config
HOST = '127.0.0.1'
PORT = 5000
DEBUG = True

# Database configuration
# Production DB
# HOST = "us-cdbr-iron-east-03.cleardb.net"
# DATABASE_NAME = "heroku_b0692bbbba2a643"
# PORT = 3306
# USERNAME = "b366db0b05b78c"
# PASSWORD = "3a9b0e26"

# Local DB
DB_HOST = "127.0.0.1"
DB_PORT = 3606
USERNAME = "root"
PASSWORD = "root"
DATABASE_NAME = "textrade-local"

SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://"
    "{username}:{password}@{host}/{dbname}".format(
        username=USERNAME, password=PASSWORD,
        host=DB_HOST, port=DB_PORT, dbname=DATABASE_NAME
    )
)

SQLALCHEMY_TRACK_MODIFICATIONS = True

THREADS_PER_PAGE = 2

CSRF_ENABLED = True

CSRF_SESSION_KEY = "a*#(!'!<S>?>:=-LA<lSD@!"

SECRET_KEY = "&!*#S<.,>,E-0oPQW??//CplQ{T}"

DOMAIN_NAME = "http://{HOST}:{PORT}".format(HOST=HOST, PORT=5000)

SENDGRID_API_KEY = "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"


def init_project(app, db, reset=False):
    if reset:
        app.logger.info("Resetting Database")
        app.logger.info("Dropping Tables...")
        db.drop_all()
        app.logger.info("Tables Dropped")
        app.logger.info("Creating Tables")
        db.create_all()
        app.logger.info("Tables Created")

        create_user_roles(app, db)


def create_user_roles(app, db):
    from app.user.models import UserRole
    app.logger.info("Creating Roles")
    db.session.add(UserRole('customer'))
    db.session.add(UserRole('developer'))
    db.session.add(UserRole('admin'))
    db.session.commit()
    app.logger.info("Roles created")
