# def get_currently_renting_out(username):
#     """This function gets the book that the passed user is
#     currently renting out.
#     """
#     return BookRenting.select().where(BookRenting.renter == username)
#
#
# def get_renting_request_by_id(request_id):
#     """This function gets a renting request by request_id"""
#     return BookRentingRequest.get(BookRentingRequest.id == request_id)
#
#
# def get_user_renting_incoming_requests(username):
#     """This function gets all the requests receipt by an specific user"""
#     return BookRentingRequest.select().where(
#         BookRentingRequest.renter == username
#     )
#
#
# def get_user_renting_outgoing_request(username):
#     """This function gets all the request sent from an specific user."""
#     return BookRentingRequest.select().where(
#         BookRentingRequest.rentee == username
#     )
#
#
# def delete_book_rent(book_id):
#     """This function delete a book for rent."""
#     BookToRent.get(BookToRent.id == book_id).delete_instance()
#
#
# def create_book_trade(**kwargs):
#     """Crate a book to trade"""
#     BookTradeWant.create(
#         name=kwargs['want_name'],
#         isbn=kwargs['want_isbn'],
#         user=kwargs['user'],
#     )
#     BookTradeHave.create(
#         name=kwargs['have_name'],
#         isbn=kwargs['have_isbn'],
#         user=kwargs['user']
#     )
#
#
# def load_book_info(isbn):
#     """Get an ISBN and return a dictionary with book information."""
#     data = requests.get("https://www.googleapis.com/books/v1/volumes?q={}".format(isbn)).json()
#     if data['totalItems']:
#         try:
#             description = data['items'][0]['volumeInfo']['description']
#         except KeyError:
#             description = "No description available."
#         book = {
#             'title': data['items'][0]['volumeInfo']['title'],
#             'authors': ', '.join(data['items'][0]['volumeInfo']['authors']),
#             'description': description,
#             'isbn': isbn,
#         }
#         return book
#     return None
#
#
# def get_book_rent(book_pk):
#     return BookToRent.get(BookToRent.id == book_pk)
#
#
# def add_to_wishlist(book_pk, username):
#     """This function add a book to the wish if not duplicate."""
#     try:
#         wishlist = WishList.get((WishList.username == username) & (WishList.book == book_pk))
#     except DoesNotExist:
#         book = BookToRent.get(BookToRent.id == book_pk)
#         if not book.username.username == username:
#             WishList.create(
#                 book=book_pk,
#                 username=username,
#             )
#         else:
#             raise SelfBook
#     else:
#         raise DuplicateEntry
