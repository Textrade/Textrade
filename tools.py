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
        If you decorate a view with this, it will ensure that the current user is
        logged in and authenticated before calling the actual view. (If they are
        not, it calls the :attr:`LoginManager.unauthorized` callback.) For
        example::

            @app.route('/post')
            @login_required
            def post():
                pass

        If there are only certain times you need to require that your user is
        logged in, you can do so with::

            if not current_user.is_authenticated():
                return current_app.login_manager.unauthorized()

        ...which is essentially the code that this function adds to your views.

        It can be convenient to globally turn off authentication when unit
        testing. To enable this, if either of the application
        configuration variables `LOGIN_DISABLED` or `TESTING` is set to
        `True`, this decorator will be ignored.

        :param func: The view function to decorate.
        :type func: function
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
