from flask import request

from app import db
from app.api.auth import auth
from app.domain.User import User
from app.jwt_utils import JWTUtils


@auth.route('/login', methods=['POST'])
def login_post():
    data = request.json
    username = data['username']
    password = data['password']
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return {"error": "Invalid credentials"}
    return {"token": JWTUtils.create_token(username=username)}


@auth.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    first_name = data['first_name']
    last_name = data['last_name']
    about_me = data['about_me']
    email = data['email']
    user = User(username=username, password=password, email=email, first_name=first_name, last_name=last_name, about_me=about_me)
    user.user_password = password
    db.session.add(user)
    db.session.commit()
    return {"message": "Registered successfully"}
