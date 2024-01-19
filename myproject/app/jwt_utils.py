from datetime import datetime, timedelta
import datetime as dt
from functools import wraps

import jwt

from flask import current_app as app, request


class JWTUtils:
    __SECRET_KEY = app.config.get("SECRET_KEY")
    __ALGORITHM = "HS256"

    @staticmethod
    def create_token(username: str):
        return jwt.encode(payload={
            'exp': datetime.utcnow() + timedelta(hours=2),
            'iat': datetime.utcnow(),
            'sun': username
        }, key=JWTUtils.__SECRET_KEY, algorithm=JWTUtils.__ALGORITHM)

    @staticmethod
    def verify_token(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = request.headers.get('Authorization')
            print("GIGA NIGGA ")
            print(token)
            if not token:
                return {'error': 'Token was not found'}, 401

            try:
                jwt.decode(token[len("Bearer "):], JWTUtils.__SECRET_KEY, algorithms=[JWTUtils.__ALGORITHM])
            except jwt.ExpiredSignatureError:
                return {'error': 'Token is expired'}, 401
            except jwt.InvalidTokenError:
                return {'error': 'Invalid token'}, 401

            return func(*args, **kwargs)

        return wrapper