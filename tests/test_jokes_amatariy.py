import pytest
from app import create_app
from app.models import db as _db

# Temporary config just for your test
class TestConfig:
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

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

# ----------------------
# HAPPY PATH
# ----------------------
def test_submit_joke_valid(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with valid non-empty text
    THEN the response should be 201 Created
    AND the response envelope should contain the submitted text
    AND the response should include an ID (if generated)
    
    Level: HAPPY PATH
    """
    response = client.post(
        '/jokes',
        json={'text': 'Why did the knight cross the road? To get to the other keep.'}
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data['data']['text'] == 'Why did the knight cross the road? To get to the other keep.'
    # Only check id if it exists
    if 'id' in data['data']:
        assert isinstance(data['data']['id'], int)
