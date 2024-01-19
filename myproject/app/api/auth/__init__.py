from flask import Blueprint


auth = Blueprint('auth', __name__)

from . import controller

@auth.errorhandler
def handle_auth_error(status):
    return "Failure to authenticate", status
