import pytest
from app.models import User, db

def test_register_happy_path(client, app):
    "Level: Happy Path - Register a new user with valid credentials."
    response = client.post('/register', json={
        'username': 'newteller',
        'password': 'securepassword123'
    })
  
    assert response.status_code == 201
    assert response.get_json()['username'] == 'newteller'
    
    with app.app_context():
        user = User.query.filter_by(username='newteller').first()
        assert user is not None
        assert user.role == 'joke-teller'

def test_register_duplicate_user(client, app):
    "Level: Edge Case - Register with a username that already exists."
    client.post('/register', json={'username': 'duplicate', 'password': 'pw1'})
    response = client.post('/register', json={'username': 'duplicate', 'password': 'pw2'})
    assert response.status_code == 409
    assert 'error' in response.get_json()

def test_admin_access_forbidden_for_teller(authenticated_client):
    "Level: Error Case - Access GET /admin/users as a joke-teller."
    response = authenticated_client.get('/admin/users')
    assert response.status_code == 403
    assert response.get_json()['error'] == 'Forbidden'

def test_admin_access_unauthorized_logged_out(client):
    "Level: Error Case - Access GET /admin/users without logging in."
    response = client.get('/admin/users')
    assert response.status_code == 401
