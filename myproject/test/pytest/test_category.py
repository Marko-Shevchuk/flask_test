from flask import url_for


def test_add_category(test_client, db, login_default_user):
    data = {
        'name': 'Test Category #4'
    }
    response = test_client.post(url_for('post.category.create_category_handle'), data=data, follow_redirects=True)
    assert response.status_code == 200
    assert 'Test Category #4' in response.text


def test_category_list(test_client, db, login_default_user):
    response = test_client.get(url_for('post.category.category_list'))
    assert [category_name in response.text for category_name in ['Test Category #1']]


def test_update_category_page(test_client, db, login_default_user):
    response = test_client.get(url_for('post.category.update_category', id=1))
    assert response.status_code == 200
    assert 'Test Category #1' in response.text


def test_update_category(test_client, db, login_default_user):
    data = {
        'name': 'Test Category #5'
    }
    response = test_client.post(url_for('post.category.update_category_handle', id=1), data=data, follow_redirects=True)
    assert data['name'] in response.text


def test_delete_category(test_client, db, login_default_user):
    response = test_client.get(url_for('post.category.delete_category', id=3), follow_redirects=True)
    assert response.status_code == 200
    assert 'You successfully deleted ur category.' in response.text