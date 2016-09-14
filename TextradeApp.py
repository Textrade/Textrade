# @app.errorhandler(404)
# def page_not_page(e):
#     return render_template('misc/404.html'), 404, e
#
#
# @app.errorhandler(500)
# def internal_error(e):
#     return "We have a internal error =(", e
#
#
# @app.route('/user/forgot/', methods=('POST', 'GET'))
# def forgot_credentials():
#     form = ForgotCredentialReset()
#     if form.validate_on_submit():
#         email = form.university_email.data
#         try:
#             user = models.User.get(models.User.university_email == email)
#         except models.DoesNotExist:
#             flash("This email is not in our system")
#             return redirect(url_for('login'))
#         token = generate_confirmation_token(email, app.secret_key)
#         html = render_template(
#             'email/forgotPassword/forgotPassword.html',
#             token=token,
#             name=user.first_name
#         )
#         subject = "Reset password request"
#
#         msg = Message(
#             subject,
#             recipients=[email],
#             html=html,
#             sender=app.config['MAIL_SENDER']
#         )
#         MAIL.send(msg)
#
#         flash("We've sent you an email with a link to reset your password.")
#         return redirect(url_for('login'))
#     for errors in form.errors.items():
#         for error in errors:
#             flash("{}".format(error))
#     return redirect(url_for('login'))
#
#
# @app.route('/user/forgot/<string:token>/', methods=('POST', 'GET'))
# def change_credentials(token):
#     email = confirm_token(token, app.secret_key)
#     if email:
#         try:
#             user = models.User.get(models.User.university_email == email)
#         except models.DoesNotExist:
#             flash("Something went wrong with your username.")
#             return redirect(url_for('login'))
#         form = ResetPassword()
#         if form.validate_on_submit():
#             user.update(
#                 password=generate_password_hash(form.password.data)
#             ).execute()
#             flash("Your password was reset successfully")
#             return redirect(url_for('login'))
#         # TODO: Need a page to change the password
#         return render_template('user/reset_password.html', form=form)
#     else:
#         flash("The confirmation link is invalid or has expired.", "error")
#         return redirect(url_for('login'))

# @app.route('/user/<string:username>/')
# def user_page(username):
#     user = None
#     try:
#         user = models.User.get(models.User.username == username)
#     except peewee.DoesNotExist:
#         abort(404)
#     user_rent_books = models.BookToRent.select().where(models.BookToRent.username == username)
#     return render_template('user/profile.html', user=user, rent_book=user_rent_books)
#
#
# @app.route('/search/')
# @login_required
# def search():
#     return render_template(
#         'rent/search.html',
#         rentals=models.BookToRent.select().where(
#             ~(models.BookToRent.username == get_current_user().username)
#         )
#     )
#
# #
# #   DASHBOARD
# #
#
#
# @app.route('/dashboard/')
# @login_required
# def dashboard():
#     book_rent = models.BookToRent.select().where(models.BookToRent.username == get_current_user())
#     wanted_books = models.BookTradeWant.select().where(models.BookTradeWant.user == get_current_user())
#     have_books = models.BookTradeHave.select().where(models.BookTradeHave.user == get_current_user())
#     return render_template(
#         'dashboard/index.html',
#         title="Dashboard",
#         book_for_rent=book_rent,
#         w_books=wanted_books,
#         h_books=have_books,
#     )
#
# #
# #
# #   RENTALS
# #
# #
#
#
# @app.route('/dashboard/your-rentals/')
# @app.route('/dashboard/rentals/')
# @login_required
# def your_rentals():
#     user = get_current_user()
#     return render_template(
#         'dashboard/rentals.html',
#         title="Your Rentals",
#         rental_list=get_rentals(
#             user
#         ),
#         add_rental_form=AddBookRentForm(),
#         currently_renting=get_currently_renting(user.username),
#         currently_renting_out=get_currently_renting_out(user.username)
#     )
#
#
# @app.route('/dashboard/rentals/delete/<int:book_id>', methods=('GET',))
# @login_required
# def delete_rental_book(book_id):
#     username = models.BookToRent.get(BookToRent.id == book_id).username.username
#     if get_current_user().username == username:
#         try:
#             delete_book_rent(book_id)
#         except models.DoesNotExist:
#             flash("The book that you are try to delete doesn't exists.", "error")
#         flash("Your book was delete successfully.", "success")
#     else:
#         flash("You are trying to delete a book that is not yours, this will be reported.", "error")
#         # TODO: Report this to log.
#     return redirect(url_for('your_rentals'))
#
#
# @app.route('/dashboard/rentals-requests/')
# @login_required
# def rental_requests():
#     user = get_current_user()
#     return render_template(
#         'dashboard/rental-requests.html',
#         title="Rental Requests",
#         incoming_rentals=get_user_renting_incoming_requests(user.username),
#         outgoing_rentals=get_user_renting_outgoing_request(user.username)
#     )
#
#
# @app.route('/dashboard/rentals-requests/request-book/<int:book_id>/',)
# @login_required
# def request_book(book_id):
#     try:
#         status = models.BookToRent.get(BookToRent.id == book_id).is_available()
#     except models.DoesNotExist:
#         flash("The book that you are trying to request doesn't exists", "error")
#         return redirect(url_for('rental_requests'))
#     else:
#         try:
#             models.BookRentingRequest.get(
#                 (models.BookRentingRequest.book == book_id) &
#                 (models.BookRentingRequest.rentee == get_current_user().username)
#             )
#         except models.DoesNotExist:
#             if status:
#                 create_request_book_rent(book_id=book_id, username=get_current_user().username)
#                 flash("This book have been requested!", "success")
#                 # TODO: Send email confirmation
#                 return redirect(url_for('rental_requests'))
#             else:
#                 flash("The book that you are trying to request is not available at this time", "error")
#                 return redirect(url_for('rental_requests'))
#         else:
#             flash("You have requested this book already", "error")
#             return redirect(url_for('rental_requests'))
#
#
# @app.route('/dashboard/rentals-requests/accept-requests/<int:request_id>/')
# @login_required
# def accept_rental_request(request_id):
#     try:
#         book_request = models.BookRentingRequest.get(
#             models.BookRentingRequest.id == request_id
#         )
#     except models.DoesNotExist:
#         flash("This request doesn't exists", "error")
#         return redirect(url_for('rental_requests'))
#     else:
#         book = models.BookToRent.get(
#             models.BookToRent.id == book_request.book
#         )
#         renter = book.username
#
#         if get_current_user().username == renter.username:
#             accept_request_to_rent(request_id)
#             flash(
#                 "You have accepted this requests, you will get an email with instruction on how to proceed",
#                 "success"
#             )
#             return redirect(url_for('rental_requests'))
#         else:
#             flash("You are not the owner of this book.")
#             return redirect(url_for('rental_requests'))
#
#
# @app.route('/dashboard/rentals-requests/delete-request/<int:request_id>/')
# @login_required
# def delete_rental_request(request_id):
#     try:
#         delete_request_book_rent(request_id, get_current_user().username)
#     except models.DoesNotExist:
#         flash("This request doesn't exists", "error")
#         return redirect(url_for('rental_requests'))
#     flash("The request was deleted successfully", "success")
#     return redirect(url_for('rental_requests'))
#
#
# @app.route('/rent/')
# def rent():
#     return render_template('rent/rent.html')
#
#
# @app.route('/rent/book/')
# def rent_all_book():
#     book = models.BookToRent.select()
#     return "All book for rent available..."
#
#
@app.route("/dashboard/rentals/add", methods=('GET', 'POST'))
@login_required
def add_book_rent():
    rent_book_form = AddBookRentForm()
    # Add a book for rent
    if rent_book_form.validate_on_submit():
        # Get ISBN from form after validate
        isbn = rent_book_form.isbn.data
        # Try to load information
        book = load_book_info(isbn)
        if book:
            # file = request.files['img']
            # if file and allowed_file(file.filename, BOOK_IMG_EXTENTIONS):
            #     # Secure the input file
            #     filename = secure_filename(
            #         "{}-{}.{}".format(
            #             flask_login.current_user.username,
            #             uuid.uuid4(),
            #             file.filename.rsplit('.', 1)[1]
            #         )
            #     )
            #     # Save the image to the server
            #     img_path = DOMAIN_NAME + '/static/img/books/' + filename
            #     file.save(os.path.join(UPLOAD_FOLDER, filename))

            # Create a book record in the database
            create_book_rent(
                name=book['title'],
                author=book['authors'],
                description=book['description'],
                isbn=isbn,
                condition=rent_book_form.condition.data,
                condition_comment=rent_book_form.condition_comment.data,
                username=get_current_user().username,
                marks=rent_book_form.marks.data,
                # img_path=img_path
            )
            flash("You book have been created!", "success")
            return redirect(url_for('add_book_rent'))
            # else:
            #     flash("This format of the file is not allowed.", "error")
        else:
            flash("We couldn't find this book, check the ISBN number.", "error")
            return redirect(url_for('add_book_rent'))

    for errors in rent_book_form.errors.items():
        for error in errors[1]:
            flash("{}".format(error))
    return redirect(url_for('your_rentals'))
#
#
# @app.route('/rent/book/<string:username>/')
# def rent_user_book(username):
#     try:
#         user = models.User.get(models.User.username == username)
#     except peewee.DoesNotExist:
#         abort(404)
#     book_for_rent = models.User.select().where(models.BookToRent.username == username)
#     return "Book for rent for a particular user."
#
#
# @app.route('/rent/book/<int:book_pk>/')
# def book_page(book_pk):
#     try:
#         user = get_user(book_pk)
#     except peewee.DoesNotExist:
#         abort(404)
#
#     user_books = models.BookToRent.select().where(models.BookToRent.username == user.username)
#
#     try:
#         book_ = models.BookToRent.get(models.BookToRent.id == book_pk)
#     except peewee.DoesNotExist:
#         abort(404)
#
#     other_equal_books = models.BookToRent.select().where(models.BookToRent.isbn == book_.isbn)
#
#     return render_template(
#         'book/book.html',
#         user=user,
#         user_books=user_books,
#         book=book_,
#         other_equal_books=other_equal_books,
#         joined=user.joined_to_string()
#     )
#
#
# @app.route('/rent/book/delete/<int:book_pk>')
# @login_required
# def delete_book(book_pk):
#     book_owner = get_user(book_pk)
#     # Check if the user logged in match the book onwer.
#     if book_owner.username == get_current_user():
#         try:
#             models.BookToRent.get(BookToRent.id == book_pk).delete_instance()
#         except models.DoesNotExist:
#             flash("This book doesn't exists.")
#         flash("The book have been deleted.")
#         return redirect(url_for('dashboard'))
#     flash("You are not the owner of this book.", "error")
#     return redirect(url_for('book_page', book_pk=book_pk))
#
#
# @app.route('/rent/book/wishlist/add/<int:book_pk>/')
# @login_required
# def wishlist_add(book_pk):
#     c_user = flask_login.current_user.username
#     try:
#         add_to_wishlist(book_pk, c_user)
#     except peewee.DoesNotExist:
#         abort(404)
#     except DuplicateEntry:
#         flash("This book is already in your wishlist!", "error")
#         return redirect(url_for('book_page', username=c_user, book_pk=book_pk))
#     except SelfBook:
#         flash("This is your own book, you can't add it", "error")
#         return redirect(url_for('book_page', username=c_user, book_pk=book_pk))
#     flash("Book added to your wishlist!", "success")
#     return redirect(url_for('book_page', username=c_user, book_pk=book_pk))
#
#
# #
# #
# #   TRADES
# #
# #
#
#
# @app.route('/dashboard/trades/')
# @login_required
# def trades():
#     return render_template(
#         'dashboard/trades.html',
#         add_have_trade_book_form=AddHaveBookTrade(),
#         add_want_trade_book_form=AddWantBookTrade(),
#         have_books=BookTradeHaveController.trade_get_all_have(
#                 get_current_user().username),
#         want_books=BookTradeWantController.trade_get_all_want(
#                 get_current_user().username),
#         title="Trades",
#     )
#
#
# @app.route('/dashboard/trades/add-have-book/', methods=('GET', 'POST'))
# @login_required
# def add_have_book():
#     have_form = AddHaveBookTrade()
#     if have_form.validate_on_submit():
#         try:
#             BookTradeHaveController.create_have_book(
#                 isbn=have_form.isbn.data,
#                 title=Tools.load_book_info(have_form.isbn.data)['title'],
#                 user=get_current_user().username
#             )
#         except TypeError:
#             flash("Please check the ISBN number, apparently this book doesn't exists.")
#
#     for errors in have_form.errors.items():
#         for error in errors[1]:
#             flash("{}".format(error))
#     return redirect(url_for('trades'))
#
#
# @app.route('/dashboard/trades/delete-have-book/<int:have_book_id>', methods=('GET', 'POST'))
# @login_required
# def delete_have_book(have_book_id):
#     try:
#         book = BookTradeHaveController.get_book_by_id(have_book_id)
#     except DoesNotExist:
#         flash("This book is not related with your account")
#         return redirect(url_for('trades'))
#     if book.user_id == get_current_user().username:
#         BookTradeHaveController.delete(have_book_id)
#         flash("Book deleted")
#     else:
#         flash("This book is not related with your account")
#     return redirect(url_for('trades'))
#
#
# @app.route('/dashboard/trades/add-want-book/', methods=('GET', 'POST'))
# @login_required
# def add_want_book():
#     want_form = AddWantBookTrade()
#     if want_form.validate_on_submit():
#         try:
#             BookTradeWantController.create_want_book(
#                 isbn=want_form.isbn.data,
#                 title=Tools.load_book_info(want_form.isbn.data)['title'],
#                 user=get_current_user().username
#             )
#         except TypeError:
#             flash("Please check the ISBN number, apparently this doesn't exists.")
#
#     for errors in want_form.errors.items():
#         for error in errors[1]:
#             flash("{}".format(error))
#     return redirect(url_for('trades'))
#
#
# @app.route('/dashboard/trades/delete-want-book/<int:want_book_id>', methods=('GET', 'POST'))
# @login_required
# def delete_want_book(want_book_id):
#     try:
#         book = BookTradeWantController.get_book_by_id(want_book_id)
#     except DoesNotExist:
#         flash("This book is not related with your account")
#         return redirect(url_for('trades'))
#
#     if book.user_id == get_current_user().username:
#         BookTradeWantController.delete(want_book_id)
#         flash("Book deleted")
#     else:
#         flash("This book is not related with your account")
#     return redirect(url_for('trades'))
#
#
# @app.route('/dashboard/trade-requests/')
# @login_required
# def trade_requests():
#     return render_template(
#         'dashboard/trade-requests.html',
#         title="Trade Requests",
#         trades_as_primary=TradeController().get_trades_as_primary(get_current_user().username),
#         trades_as_secondary=TradeController().get_trades_as_secondary(get_current_user().username)
#     )
#
#
# @app.route('/dashboard/trade-requests/approve/<int:trade_id>', methods=('GET', 'POST'))
# @login_required
# def approve_trade_request(trade_id):
#     if TradeController.get_primary_user(trade_id) == get_current_user().username:
#         try:
#             TradeController.approve_trade_as_user_one(trade_id)
#         except DoesNotExist:
#             flash("This trade doesn't exists.")
#             return redirect(url_for('trade_requests'))
#         flash("Trade request approved. You will receive an email with instructions.")
#     elif TradeController.get_secondary_user(trade_id) == get_current_user().username:
#         try:
#             TradeController.approve_trade_as_user_two(trade_id)
#         except DoesNotExist:
#             flash("This trade doesn't exists.")
#             return redirect(url_for('trade_requests'))
#         flash("Trade request approved. You will receive an email with instructions.")
#     else:
#         flash("This is not a request related to you")
#     return redirect(url_for('trade_requests'))
#
#
# @app.route('/dashboard/trade-requests/decline/<int:trade_id>', methods=('GET', 'POST'))
# @login_required
# def decline_trade_request(trade_id):
#     try:
#         TradeController.delete_trade(trade_id)
#     except DoesNotExist:
#         flash("This trade doesn't exists.")
#     return redirect(url_for('trade_requests'))
#
# #
# #
# #   SETTINGS
# #
# #
#
#
# @app.route('/dashboard/setting/')
# @login_required
# def account_settings():
#     return render_template(
#         'dashboard/account-settings.html',
#         title="Account Settings"
#     )
#
#
# @app.route('/dashboard/history/')
# @login_required
# def account_history():
#     return render_template(
#         'dashboard/history.html',
#         title="History"
#     )
#
#
# if __name__ == '__main__':
#     app.run(debug=DEBUG, host=HOST, port=PORT)
