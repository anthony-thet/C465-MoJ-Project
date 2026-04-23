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
def authenticated_client(client, app):
    """Returns a test client logged in via the correct API route."""
    with app.app_context():
        username = 'testuser'
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            user.set_password('testpass')
            _db.session.add(user)
            _db.session.commit()
        client.post('/api/v1/auth/login', json={
            'username': username,
            'password': 'testpass'
        })
    return client


@pytest.fixture(scope='function')
def sample_user(app):
    user = User(username='qauser')
    user.set_password('testpass')
    _db.session.add(user)
    _db.session.commit()
    return user


@pytest.fixture(scope='function')
def auth_headers(client, sample_user):
    client.post('/login', json={
        'username': 'qauser',
        'password': 'testpass'
    })
    return {}


@pytest.fixture
def admin_user(app):
    """An admin user for testing admin-only endpoints."""
    with app.app_context():
        user = User(username='admin_alice', role='admin')
        user.set_password('adminpass123')
        _db.session.add(user)
        _db.session.commit()
        yield user
        _db.session.rollback()


@pytest.fixture
def regular_user(app):
    """A non-admin user for testing role enforcement."""
    with app.app_context():
        user = User(username='regular_bob', role='user')
        user.set_password('userpass123')
        _db.session.add(user)
        _db.session.commit()
        yield user
        _db.session.rollback()


@pytest.fixture
def admin_client(client, admin_user):
    """A test client logged in as an admin."""
    client.post('/api/v1/auth/login',
                json={'username': 'admin_alice', 'password': 'adminpass123'})
    return client


@pytest.fixture
def regular_client(client, regular_user):
    """A test client logged in as a non-admin user."""
    client.post('/api/v1/auth/login',
                json={'username': 'regular_bob', 'password': 'userpass123'})
    return client


@pytest.fixture
def sample_jokes(app, admin_user):
    """Three jokes: two unflagged, one flagged."""
    with app.app_context():
        j1 = Joke(text='Why did the parrot join the ministry?',
                  submitted_by=admin_user.id,
                  flagged=False)
        j2 = Joke(text='A dead parrot is still a parrot.',
                  submitted_by=admin_user.id,
                  flagged=True)
        j3 = Joke(text='Nobody expects the Spanish Inquisition!',
                  submitted_by=admin_user.id,
                  flagged=False)
        _db.session.add_all([j1, j2, j3])
        _db.session.commit()
        yield [j1, j2, j3]


@pytest.fixture
def sample_joke(app, regular_user):
    with app.app_context():
        joke = Joke(text="Why did the parrot join the Ministry?",
                    submited_by=regular_user.id, flagged=False)
        _db.session.add(joke)
        _db.session.commit()
        yield joke
