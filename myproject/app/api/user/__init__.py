from flask import Blueprint, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from app.api.user.controller import UserController, UsersController

user = Blueprint('user', __name__)

api = Api(user, errors=user.app_errorhandler)
api.add_resource(UserController, "/", "/<int:id>")
api.add_resource(UsersController, "/list")


@user.app_errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
