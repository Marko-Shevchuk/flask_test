import json

import pytest
from flask import url_for
from app.domain.Category import Category
from app.domain.Post import Post, PostType
from app.domain.Tag import Tag
from app.domain.Todo import Status, Task
from app import create_app, db
from app.domain.User import User
from config import TestProfile


@pytest.fixture(scope='module')
def test_config():
    app = create_app(TestProfile.ENV_NAME)
    yield app


@pytest.fixture(scope='module')
def test_client(test_config):
    with test_config.test_client() as testing_client:
        with test_config.app_context():
            yield testing_client

def resolve_resources():
    current_path = os.getcwd()
    if current_path.endswith('pytest'):
        return '../'
    return 'test/'

@pytest.fixture
def db(test_config):
    db.create_all()
    """ Preparing users """
    resource_path = resolve_resources()
    with open(resource_path + 'resources/test_users.json') as users_file:
        users_data = json.load(users_file)
        for user_data in users_data:
            user = User()
            user.username = user_data['username']
            user.first_name = user_data['first_name']
            user.last_name = user_data['last_name']
            user.email = user_data['email']
            user.about_me = user_data['about_me']
            user.user_password = user_data['password']
            db.session.add(user)

        db.session.commit()
        """ Preparing tasks... """
    with open(resource_path + 'resources/test_tasks.json') as tasks_file:
        tasks_data = json.load(tasks_file)
        for task_data in tasks_data:
            task = Task()
            task.name = task_data['name']
            task.status = Status[task_data['status']]
            task.description = task_data['description']
            db.session.add(task)

        db.session.commit()

    """ Preparing Tags... """
    with open(resource_path + 'resources/test_tags.json') as tags_file:
        tag_data = json.load(tags_file)
        for tag_data in tag_data:
            tag = Tag()
            tag.name = tag_data['name']
            tag.color = tag_data['color']
            db.session.add(tag)

        db.session.commit()

    """ Preparing Categories... """
    with open(resource_path + 'resources/test_categories.json') as categories_file:
        category_data = json.load(categories_file)
        for category_data in category_data:
            category = Category()
            category.name = category_data['name']
            db.session.add(category)

        db.session.commit()

    with open(resource_path + 'resources/test_posts.json') as posts_file:
        posts_data = json.load(posts_file)
        for post_data in posts_data:
            post = Post()
            post.title = post_data['title']
            post.text = post_data['text']
            post.enabled = post_data['enabled']
            post.type = PostType[post_data['type']]
            post.user_id = post_data['user_id']
            post.category_id = post_data['category_id']
            db.session.add(post)

        db.session.commit()
    yield
    db.session.remove()
    db.drop_all()


@pytest.fixture
def login_default_user(test_client):
    test_client.post(url_for('auth.login_handle'),
                     data={'login': 'user2', 'password': '12345Jeez', 'remember': True},
                     follow_redirects=True)
    yield
    test_client.get(url_for('auth.logout'))

@pytest.fixture
def login_default_second_user(test_client):
    test_client.post(url_for('auth.login_handle'),
                     data={'login': 'adam', 'password': '12345Gee', 'remember': True},
                     follow_redirects=True)
    yield
    test_client.get(url_for('auth.logout'))