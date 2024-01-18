from flask import Blueprint

general_bp = Blueprint("general", __name__, template_folder="templates", static_folder="static")

from . import controller