import json

import pytest
from flask_login import login_user, logout_user

from app import create_app, db
from app.domain.User import User
from config import TestProfile


@pytest.fixture
def test_config():
    app = create_app(TestProfile.ENV_NAME)
    yield app


@pytest.fixture
def test_client(test_config):
    with test_config.test_client() as testing_client:
        with test_config.app_context():
            yield testing_client


@pytest.fixture
def db(test_config):
    db.create_all()
    with open('../../resources/test_users.json') as users_file:
        users_data = json.load(users_file)
        for user_data in users_data:
            user = User()
            user.username = user_data['username']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            user.birth_date = user_data['birth_date']
            user.about_me = user_data['about_me']
            user.user_password = user_data['password']
            db.session.add(user)

        db.session.commit()
    yield
    db.session.remove()
    db.drop_all()


@pytest.fixture
def login_default_user():
    login_user(User.query.get(1), remember=True)
    yield
    logout_user()