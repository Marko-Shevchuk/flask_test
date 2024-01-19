from flask import request
from flask_restful import Resource

from app import db
from app.jwt_utils import JWTUtils
from app.domain.User import User
from app.api.user.schemes import UsersSchema, UserCreateSchema


class UserController(Resource):
    @JWTUtils.verify_token
    def get(self, id):
        user = User.query.get(id)
        return UsersSchema().dump(user), 200

    @JWTUtils.verify_token
    def post(self):
        schema = UserCreateSchema()
        entity = schema.load(request.json)
        db.session.add(entity)
        db.session.commit()
        return UsersSchema().dump(entity), 201

    @JWTUtils.verify_token
    def put(self, id):
        user = User.query.get(id)
        schema = UsersSchema()
        entity = schema.load(request.json, instance=user)
        db.session.commit()
        return schema.dump(entity), 200

    @JWTUtils.verify_token
    def delete(self, id):
        user = User.query.get(id)
        db.session.delete(user)
        db.session.commit()
        return {}, 204



class UsersController(Resource):
    @JWTUtils.verify_token
    def get(self):
        return UsersSchema(many=True).dump(User.query.all())
