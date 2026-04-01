import pytest
from app import create_app
<<<<<<< HEAD
from app.models import db as _db, User
=======
from app.models import db as _db, User, Joke
>>>>>>> f4474f9 (QA Sentinel: add rating tests and fixtures)


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
<<<<<<< HEAD


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
=======
@pytest.fixture(scope='function')
def sample_user(app):
    user = User(
        username='testuser',
        password_hash='fakehash'
    )
    _db.session.add(user)
    _db.session.commit()
    return user


@pytest.fixture(scope='function')
def sample_joke(app, sample_user):
    joke = Joke(
        text='Why did the QA engineer cross the road? To reproduce the bug.',
        submitted_by=sample_user.id
    )
    _db.session.add(joke)
    _db.session.commit()
    return joke


@pytest.fixture(scope='function')
def auth_headers(client, sample_user):
    return {}
>>>>>>> f4474f9 (QA Sentinel: add rating tests and fixtures)
