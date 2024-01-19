import unittest

from flask import url_for
from flask_login import current_user

from test.base_test import BaseTest


class UserTest(BaseTest):

    def test_change_user_data(self):
        """
        This test checks if user can change their data
        Sign in first
        """
        with self.client:
            login_user_data = {
                'login': 'user2',
                'password': '12345Jeez',
                'remember': True
            }

            response = self.client.post(url_for('auth.login_handle'), data=login_user_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'You successfully logged in.', response.data)
            self.assertTrue(current_user.is_authenticated)

            change_data = {
                'first_name': 'Firstnameuserone',
                'last_name': 'Lastnameuserone',
                'about_me': 'Another string about me.',

                'email': 'u@gmail.com',
                'username': 'u'
            }

            response = self.client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn(b'ccessfully', response.data)
            self.assertIn(change_data['first_name'], response.text)
            self.assertIn(change_data['last_name'], response.text)
            self.assertIn(change_data['about_me'], response.text)

    def test_change_user_data_with_email_and_username(self):
        """
        This test checks if user can change their data
        As well checks changing their email and username
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
            self.assertTrue(current_user.is_authenticated)

            change_data = {
                'first_name': 'Firstnameuser',
                'last_name': 'Lastnameuser',
                'about_me': 'string about me.',
                'email': 'u2@gmail.com',
                'username': 'uj2'
            }

            response = self.client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("exist", response.text)

            change_data['email'] = 'u2dddd@gmail.com'
            change_data['username'] = 'u2'
            response = self.client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
            self.assert200(response)
            self.assertIn("exist", response.text)


if __name__ == 'main':
    unittest.main()