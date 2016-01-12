import requests
from functools import wraps

from flask import current_app
from werkzeug.local import LocalProxy
from flask_login import current_user


class Tools:
    @staticmethod
    def load_book_info(isbn):
        """Get an ISBN and return a dictionary with book information."""
        data = requests.get("https://www.googleapis.com/books/v1/volumes?q={}".format(isbn)).json()
        if data['totalItems']:
            try:
                description = data['items'][0]['volumeInfo']['description']
            except KeyError:
                description = "No description available."
            book = {
                'title': data['items'][0]['volumeInfo']['title'],
                'authors': ', '.join(data['items'][0]['volumeInfo']['authors']),
                'description': description,
                'isbn': isbn,
            }
            return book
        return None

    @staticmethod
    def admin_required(func):
        """
        This method is a type of login_required decorator but for admin
        required areas. This doesn't allows any type of user to access
        areas that they are shouldn't be looking.

        You can decorator any view with this method, for example;

        @Tools.admin_required
        @app.route('/top-secret/
        def top_secret_view():
            return "Welcome admin!"
        """

        @wraps(func)
        def decorated_view(*args, **kwargs):
            if current_user.is_anonymous():
                return current_app.login_manager.unauthorized()
            else:
                if current_user.is_admin():
                    return func(*args, **kwargs)
                else:
                    return current_app.login_manager.unauthorized()
        return decorated_view
