from flask import Blueprint

todo_rest_bp = Blueprint("todo_rest", __name__)

from . import controller