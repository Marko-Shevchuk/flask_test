from marshmallow import fields, validate, validates_schema, ValidationError

from app import mm
from app.domain.User import User


class UsersSchema(mm.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
    id = fields.Integer(dump_only=True)
    username = fields.String(required=True, validate=[validate.Length(1,32)])
    first_name = fields.String(required=True, validate=[validate.Length(1,32)])
    last_name = fields.String(required=True, validate=[validate.Length(1,32)])
    password = fields.String(required=True, validate=[validate.Length(8,256)])
    email = fields.String(required=True, validate=[validate.Length(1,256)])
    about_me = fields.String(required=False, validate=[validate.Length(max=512)])
    @validates_schema
    def validate_email(self, data, **kwargs):
        id = data.get('id')
        email = data.get('email')
        user = User.query.filter_by(email = email).first()
        if not user:
            return
        if user.id != id:
            raise ValidationError('Email already exists')

    @validates_schema
    def validate_username(self, data, **kwargs):
        id = data.get('id')
        username = data.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            return
        if user.id != id:
            raise ValidationError('Username already exists')

class UserCreateSchema(UsersSchema):
    password = fields.String(required=True)