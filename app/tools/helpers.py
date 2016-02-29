#
#   Helper functions
#
#
from flask import flash


def flash_from_errors(form):
    for errors in form.errors.items():
        for error in errors[1]:
            flash("{}".format(error))