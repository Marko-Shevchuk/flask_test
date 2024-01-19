from flask import Blueprint

from app.api.auth import auth


api = Blueprint('api', __name__)
api.register_blueprint(auth, url_prefix='/auth')
