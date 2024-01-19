from flask import Blueprint

from app.api.auth import auth
from app.api.user import user

api = Blueprint('api', __name__)

api.register_blueprint(auth, url_prefix='/auth')
api.register_blueprint(user, url_prefix='/user')
