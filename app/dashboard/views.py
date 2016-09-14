from flask import Blueprint, render_template
from flask_login import login_required

from app.book.book import BookRentController
from app.book.forms import AddBookRentForm
from app.user.views import get_current_user

dashboard = Blueprint('dashboard', __name__)


@dashboard.route('/dashboard/')
def index():
    return render_template(
        'dashboard/index.html',
        title="Dashboard",
        book_for_rent=[0, 1, 2],
        w_books=[0, 1, 2],
        h_books=[0, 1, 2]
    )


@dashboard.route('/dashboard/your-rentals/')
@login_required
def your_rentals():
    user = get_current_user()
    return render_template(
        'dashboard/rentals.html',
        title="Your Rentals",
        rental_list=None,
        add_rental_form=AddBookRentForm(),
        currently_renting=BookRentController.get_available_rentals(user.username),
        currently_renting_out=BookRentController.get_currently_renting_out(user.id)
    )


@dashboard.route('/dashboard/rentals-requests/')
def rental_requests():
    user = get_current_user()
    return render_template(
        'dashboard/rental-requests.html',
        title="Rental Request"
    )


@dashboard.route('/trades/')
def trades():
    return render_template(
        'dashboard/trade-requests.html',
        title="Trades"
    )


@dashboard.route('/dashboard/trade-requests/')
def trade_requests():
    return render_template(
        'dashboard/trade-requests.html',
        title="Trade Requests"
    )


@dashboard.route('/dashboard/setting/')
def account_settings():
    return render_template(
        'dashboard/account-settings.html',
        title="Account Settings"
    )


@dashboard.route('/dashboard/history')
def account_history():
    return render_template(
        'dashboard/history.html',
        title="Account History"
    )
