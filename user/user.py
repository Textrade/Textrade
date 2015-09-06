import datetime

from flask.ext.bcrypt import check_password_hash, generate_password_hash

from models import User, db


def create_user(**kwargs):
    """"Create user controls."""
    User.create(
        first_name=kwargs['first_name'],
        last_name=kwargs['last_name'],
        username=kwargs['username'],
        password=kwargs['password'],
        # university_name=kwargs['university_name'],
        university_email=kwargs['university_email'],
        personal_email=kwargs['personal_email']
    )


def change_user_password(pk_id, old_password, new_password):
    """Edit a user."""
    user = User.get(User.id == pk_id)

    if check_password_hash(user.password, old_password):
        user.update(password=generate_password_hash(new_password)).execute()
    else:
        raise PermissionError("Invalid password.")


def delete_user(username, password):
    """Delete a user. The password must be provided."""
    user = User.get(User.username == username)
    if check_password_hash(
        user.password,
        password
    ):
        user.delete_instance()
    else:
        raise PermissionError("Invalid password.")
