from flask.ext.bcrypt import check_password_hash, generate_password_hash

from .models import User
from app import db

# Alchemy Tools
import sqlalchemy as sql


class UserController:

    def __init__(self, first_name=None, last_name=None,
                 username=None, password=None, university_email=None,
                 role="customer", user=None):
        self.user = user  # This is the user object
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = UserController.__get_hash(password)
        self.university_email = university_email
        self.role = role

    @staticmethod
    def create_user(**kwargs):
        """"Create user controls."""
        db.session.add(
            User(
                first_name=kwargs['first_name'],
                last_name=kwargs['last_name'],
                username=kwargs['username'],
                password=kwargs['password'],
                # TODO: when expansion to different schools
                university_email=kwargs['university_email'],
                role="costumer"
            )
        )
        db.session.commit()

    def create(self):
        """Create user if initialized with constructor."""
        db.session.add(
            User(self.first_name, self.last_name, self.username,
                 self.password, self.university_email, self.role)
        )
        db.session.commit()

    def change_password(self, old_password, new_password):
        """Change the user passed in constructor."""
        if UserController.__check_hash(self.password, new_password):
            db.session.execute(
                sql.update(self.user).where(
                    User.username == self.username
                ).values(
                    password=UserController.__get_hash(new_password)
                )
            )
            db.session.commit()
        else:
            raise ValueError("Old password is invalid.")

    @staticmethod
    def change_user_password(pk_id, old_password, new_password):
        """Edit a user. Old password is required."""
        user = User.query.filter_by(id=pk_id).first()

        if UserController.__check_hash(user.password, old_password):
            db.session.execute(
                sql.update(User).where(
                    User.id == pk_id
                ).values(
                    password=generate_password_hash(new_password)
                )
            )
            db.session.commit()
        else:
            raise ValueError("Old password is invalid.")

    @staticmethod
    def delete_user(username, password):
        """Delete a user. The password must be provided."""
        user = User.get(User.username == username)
        if UserController.__check_hash(
            user.password,  # Hash
            password
        ):
            user.delete_instance()
        else:
            raise PermissionError("You password is wrong.")

    @staticmethod
    def __get_hash(password):
        return generate_password_hash(password)

    @staticmethod
    def __check_hash(p_hash, password):
        return check_password_hash(p_hash, password)
