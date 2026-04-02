import pytest
from app import create_app
from app.models import db as _db, User


class TestConfig:
    TESTING = True


@pytest.fixture(scope='function')
def app():
    application = create_app(TestConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture
def authenticated_client(client, app):
    """Returns a test client logged in as a joke-teller."""
    with app.app_context():
        user = User(username='testuser')
        user.set_password('testpass')
        _db.session.add(user)
        _db.session.commit()
        client.post('/login', json={
            'username': 'testuser',
            'password': 'testpass'
        })
    return client
