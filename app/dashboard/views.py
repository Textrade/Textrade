from flask import (Blueprint, request, render_template, flash,
                   redirect, url_for)

from app.user.views import get_current_user
from app.user.user import UserController

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


@dashboard.route('/your_rentals/')
def your_rentals():
    user = get_current_user()
    return render_template(
        'dashboard/rentals.html',
        title="Your Rentals",
        rental_list=[0, 1, 2],
        add_rental_form=None,
        currently_renting=[0, 1, 2],
        currently_renting_out=[0, 1, 2]
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
