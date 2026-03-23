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


# ----------------------
# EDGE CASE
# ----------------------
def test_submit_joke_max_length(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with text exactly 500 characters long
    THEN the response should be 201 Created
    AND the stored text should not be truncated

    Level: EDGE CASE
    """
    max_text = 'A' * 500
    response = client.post('/jokes', json={'text': max_text})
    assert response.status_code == 201
    data = response.get_json()
    assert len(data['data']['text']) == 500


# ----------------------
# ERROR CASE
# ----------------------
def test_submit_joke_empty_text(client):
    """
    GIVEN a running MoJ application
    WHEN a POST request is made to /jokes with empty text
    THEN the response should be 400 Bad Request

    Level: ERROR CASE
    """
    response = client.post('/jokes', json={'text': ''})
    assert response.status_code == 400
