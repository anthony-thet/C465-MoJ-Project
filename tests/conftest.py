import pytest
from app import create_app
from app.models import db as _db, User, Joke


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
def authenticated_client(client, seed_user, seed_joke):
    """A test client logged in as seed_user who has submitted a joke."""
    client.post('/api/v1/auth/login',
                json={'username': 'alice', 'password': 'correctpassword'})
    return client


@pytest.fixture(scope='function')
def sample_user(app):
    user = User(username='qauser')
    user.set_password('testpass')
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
    client.post('/login', json={
        'username': 'qauser',
        'password': 'testpass'
    })
    return {}
