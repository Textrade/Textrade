from app import db
from app.user.models import User
from app.user.user import UserController
# from app.book.models import BookToRent

# Alchemy ORM Tools
import sqlalchemy as sql


class DashBoardController:
    def __init__(self, user):
        # If user doesn't exist, will raise a UserNotFound exception
        UserController.get_user_by_username(user.username)

        self.user = user
