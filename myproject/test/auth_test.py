import unittest

from flask import url_for
from flask_login import current_user

from app.domain.User import User
from test.base_test import BaseTest


class AuthTest(BaseTest):

    def test_register_success(self):
        """
        Checks if the user is correctly saved to the database.
        """

        with self.client:
            register_user_data = {
                'username': 'user3',
                'first_name': 'Jacon',
                'last_name': 'Irv',
                'email': 'user69@gmail.com',
                'password': 'btdBATTLES123',
                'confirm_password': 'btdBATTLES123'
            }
            response = self.client.post(url_for('auth.register_handle'), data=register_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn('Successfully created account', response.text)

            expected_id = 3
            registered_user = User.query.get(expected_id)
            self.assertIsNotNone(registered_user)
            self.assertEqual(register_user_data['username'], registered_user.username)

    def test_duplicate_register(self):
        """
        Checks if user cannot sign up with already existing emails and usernames
        """
        with self.client:
            register_user_data = {
                'username': 'user3',
                'first_name': 'Firstname',
                'last_name': 'Lastname',
                'email': 'user69@gmail.com',
                'password': 'secRET123',
                'confirm_password': 'secRET123'
            }
            response = self.client.post(url_for('auth.register_handle'), data=register_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Email already exists.', response.data)

            register_user_data['email'] = 'user1@gmail.com'
            register_user_data['username'] = 'user3'
            response = self.client.post(url_for('auth.register_handle'), data=register_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Username', response.data)

    def test_login_success(self):
        """
        Checks if user can sign in with valid credentials
        """
        with self.client:
            login_user_data = {
                'login': 'adam',
                'password': '12345Gee',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'uccess', response.data)

    def test_login_with_incorrect_data(self):
        """
        Checks if user cannot sign in with invalid credentials
        """
        with self.client:
            login_user_data = {
                'login': 'user1',
                'password': '12',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'Invalid cred', response.data)

    def test_logout(self):
        """
        Checks if user can log out
        """
        with self.client:
            login_user_data = {
                'login': 'user2',
                'password': '12345Jeez',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'uccess', response.data)

            self.assertTrue(current_user.is_authenticated)
            response = self.client.get(url_for('auth.logout'), follow_redirects=True)
            self.assert200(response)


if __name__ == 'main':
    unittest.main()