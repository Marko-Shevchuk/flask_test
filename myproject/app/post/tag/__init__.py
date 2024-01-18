from flask import Blueprint

tag_bp = Blueprint("tag", __name__, template_folder="templates")

from . import controller