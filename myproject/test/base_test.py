import json
import unittest

from flask_testing import TestCase

from app import create_app, db
from app.domain.Todo import Task, Status
from app.domain.User import User
from config import TestProfile


class BaseTest(TestCase):

    def create_app(self):
        return create_app(TestProfile.ENV_NAME)

    def start(self):
        db.create_all()
        self.__load_users()
        self.__load_tasks()

    def end(self):
        db.session.remove()
        db.drop_all()

    def __load_users(self):
        with open('./resources/test_users.json') as users_file:
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

    def __load_tasks(self):
        with open('./resources/test_tasks.json') as tasks_file:
            tasks_data = json.load(tasks_file)
            for task_data in tasks_data:
                task = Task()
                task.name = task_data['name']
                task.status = Status[task_data['status']]
                task.description = task_data['description']
                db.session.add(task)

            db.session.commit()


if __name__ == '__main__':
    unittest.main()