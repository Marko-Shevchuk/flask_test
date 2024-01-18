from flask import Blueprint
from .category import category_bp
from .tag import tag_bp

post_bp = Blueprint("post", __name__, template_folder="templates")

post_bp.register_blueprint(category_bp, url_prefix='category')
post_bp.register_blueprint(tag_bp, url_prefix='tag')

from . import controller