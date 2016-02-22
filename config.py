import os

# Debug environment variable
DEBUG = True

# Application directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Database configurarion

# Production DB
# HOST = "us-cdbr-iron-east-03.cleardb.net"
# DATABASE_NAME = "heroku_b0692bbbba2a643"
# PORT = 3306
# USERNAME = "b366db0b05b78c"
# PASSWORD = "3a9b0e26"

# Local DB
HOST = "127.0.0.1"
PORT = 3606
USERNAME = "root"
PASSWORD = "root"
DATABASE_NAME = "textrade-local"

SQLALCHEMY_DATABASE_URI = (
    "mysql+pymysql://"
    "{username}:{password}@{host}/{dbname}".format(
            username=USERNAME, password=PASSWORD,
            host=HOST, dbname=DATABASE_NAME
    )
)

# MAIL CONFIG
# MAIL_SERER = "smtp.gmail.com"
# MAIL_PORT = 465
# MAIL_USE_SSL = True
# MAIL_SENDER = "Textrade <umltextrade@gmail.com>"
# MAIL_USERNAME = "umltextrade@gmail.com"
# MAIL_PASSWORD = "Angell100."

SQLALCHEMY_TRACK_MODIFICATIONS = True

THREADS_PER_PAGE = 2

CSRF_ENABLED = True

CSRF_SESSION_KEY = "a*#(!'!<S>?>:=-LA<lSD@!"

SECRET_KEY = "&!*#S<.,>,E-0oPQW??//CplQ{T}"

DOMAIN_NAME = "http://0.0.0.0:5000"
