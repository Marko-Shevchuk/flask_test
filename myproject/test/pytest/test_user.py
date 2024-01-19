from flask import url_for


def test_change_user_data(test_client, db, login_default_user):
    change_data = {
        'first_name': 'Firstnameuserone',
        'last_name': 'Lastnameuserone',
        'about_me': 'string about me.',
        'email': 'user1@mail.com',
        'username': 'user1'
    }

    response = test_client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)

    assert response.status_code == 200
    assert 'You successfully updated your account details!' in response.text
    assert change_data['first_name'], response.text
    assert change_data['last_name'], response.text
    assert change_data['about_me'], response.text


def test_change_user_data_with_existing_email_and_username(test_client, db, login_default_user):
    change_data = {
        'first_name': 'Firstnameuserone',
        'last_name': 'Lastnameuserone',
        'about_me': 'string about me.',
        'email': 'user2@mail.com',
        'username': 'user1'
    }

    response = test_client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
    assert response.status_code == 200
    assert "exist" in response.text

    change_data['email'] = 'user1@mail.com'
    change_data['username'] = 'user2'
    response = test_client.post(url_for('user.update_account'), data=change_data, follow_redirects=True)
    assert response.status_code == 200
    assert "exist" in response.text