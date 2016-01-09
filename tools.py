import requests


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
