from models import Trade, BookTradeHave, BookTradeWant


class TradeController:
    def __init__(self, user_one=None, user_two=None, book_one=None,
                 book_two=None, status="processing"):
        self.user_one = user_one
        self.user_two = user_two
        self.book_one = book_one
        self.book_two = book_two
        self.status = status

    def create(self):
        """Create a trade from the instance created by the constructor"""
        Trade.create(
            user_one=self.user_one,
            user_two=self.user_two,
            book_one=self.book_one,
            book_two=self.book_two,
            status=self.status
        )

    @staticmethod
    def create_trade(user_one=None, user_two=None, book_one=None,
                     book_two=None, status="processing"):
        """Static method to create trade."""
        Trade.create(
            user_one=user_one,
            user_two=user_two,
            book_one=book_one,
            book_two=book_two,
            status=status
        )

    @staticmethod
    def delete_trade(trade_id):
        Trade.get(
                Trade.id == trade_id
        ).delete_instance()

    @staticmethod
    def modify_trade_primary_user(trade_id, user):
        """This function change the primary user of a trade."""
        Trade.get(
                Trade.id == trade_id
        ).update(Trade.user_one == user).execute()

    @staticmethod
    def modify_trade_primary_user(trade_id, user):
        """This function change the secondary user of a trade."""
        Trade.get(
                Trade.id == trade_id
        ).update(Trade.user_two == user).execute()

    @staticmethod
    def modify_trade_primary_book(trade_id, book):
        """This function change the primary book of a trade."""
        Trade.get(
                Trade.id == trade_id
        ).update(Trade.book_one == book).execute()

    @staticmethod
    def modify_trade_secondary_book(trade_id, book):
        """This function change the secondary book of a trade."""
        Trade.get(
                Trade.id == trade_id
        ).update(Trade.book_two == book).execute()

    @staticmethod
    def get_trades_as_primary(username):
        """This method return a list of all trades that the passed user is a primary."""
        return Trade.select().where(Trade.user_one == username)

    @staticmethod
    def get_trades_as_secondary(username):
        """This method return a list of all trades that the passed user is a secondary."""
        return Trade.select().where(Trade.user_two == username)

    @staticmethod
    def get_all_trades_by_user(username):
        """This method return a list of all trades that the user is involved with."""
        trades = []
        as_primary = Trade.select().where(Trade.user_one == username)
        as_secondary = Trade.select().where(Trade.user_two == username)

        for t in as_primary:
            trades.append(t)
        for t in as_secondary:
            trades.append(t)
        return trades


class BookTradeHaveController:
    def __init__(self, title="", isbn="", user=""):
        self.title = title
        self.isbn = isbn
        self.user = user

    def create(self):
        BookTradeHave.create(
            name=self.title,
            isbn=self.isbn,
            user=self.user
        )

    @staticmethod
    def create_have_book(title, isbn, user):
        BookTradeHave.create(
            name=title,
            isbn=isbn,
            user=user
        )

    @staticmethod
    def modify_title(have_id, title):
        BookTradeHave.get(
                BookTradeHave.id == have_id
        ).update(BookTradeHave.name == title).execute()

    @staticmethod
    def modify_isbn(have_id, isbn):
        BookTradeHave.get(
                BookTradeHave.id == have_id
        ).update(BookTradeHave.isbn == isbn).execute()

    @staticmethod
    def delete(have_id):
        BookTradeHave.get(
            BookTradeHave.id == have_id
        ).delete_instance()

    @staticmethod
    def trade_get_all_have(username):
        return BookTradeHave.select().where(
            BookTradeHave.user == username
        )


class BookTradeWantController:
    def __init__(self, title="", isbn="", user=""):
        self.title = title
        self.isbn = isbn
        self.user = user

    def create(self):
        BookTradeWant.create(
            name=self.title,
            isbn=self.isbn,
            user=self.user
        )

    @staticmethod
    def create_want_book(title, isbn, user):
        BookTradeWant.create(
            name=title,
            isbn=isbn,
            user=user
        )

    @staticmethod
    def modify_title(have_id, title):
        BookTradeWant.get(
                BookTradeWant.id == have_id
        ).update(BookTradeWant.name == title).execute()

    @staticmethod
    def modify_isbn(have_id, isbn):
        BookTradeWant.get(
                BookTradeWant.id == have_id
        ).update(BookTradeWant.isbn == isbn).execute()

    @staticmethod
    def delete(have_id):
        BookTradeWant.get(
            BookTradeWant.id == have_id
        ).delete_instance()

    @staticmethod
    def trade_get_all_want(username):
        return BookTradeWant.select().where(
            BookTradeWant.user == username
        )
