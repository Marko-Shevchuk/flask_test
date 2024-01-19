from flask import url_for
from flask_login import login_user

from app.domain.Task import Status
from app.domain.User import User
from test.base_test import BaseTest


class TaskTest(BaseTest):

    def setUp(self):
        super().start()
        login_user(User.query.get(1))

    def test_get_all_tasks(self):
        """
        Checks if tasks are correctly displayed on page
        """
        with self.client:
            response = self.client.get(url_for('todo.tasks'))
            self.assert200(response)
            task_names = ['T1', 'T2', 'T', 'T4']
            for task_name in task_names:
                self.assertIn(task_name, response.text)

    def test_task_correct_add(self):
        """
        Checks if new task is be added correctly
        """
        with self.client:
            task_data = {
                'name': 'Task6',
                'description': 'description'
            }
            response = self.client.post(url_for('todo.add_task'), data=task_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(task_data['name'], response.text)

    def test_task_incorrect_add(self):
        """
        Checks if error will be displayed when trying to insert task with existing name
        """
        with self.client:
            task_data = {
                'name': 'T1',
                'description': 'T1',
                'status': Status.TODO
            }
            response = self.client.post(url_for('todo.add_task', id=1), data=task_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("ALREADY", response.text)



    def test_task_delete(self):
        """
        Checking task deletion
        """
        with self.client:
            response = self.client.get(url_for('task.delete_task', id=1), follow_redirects=True)
            self.assert200(response)
            self.assertIn("deleted", response.text)