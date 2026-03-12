import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_get_jokes_returns_empty_list(client):
    """
    GIVEN a fresh MoJ application with no jokes submitted
    WHEN a GET request is made to /jokes
    THEN the response is 200 OK and the jokes list is empty

    Level: HAPPY PATH
    """
    response = client.get('/jokes')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'ok'
    assert data['data']['jokes'] == []

# tests/test_jokes.py
# Three-level test suite for POST /jokes
# GIVEN/WHEN/THEN format required — Level: tag required in every docstring

def test_submit_joke_valid(client):
    """
    GIVEN ...
    WHEN ...
    THEN ...

    Level: HAPPY PATH
    """
    pass  # Phase 2 fills this in


def test_submit_joke_max_length(client):
    """
    GIVEN ...
    WHEN ...
    THEN ...

    Level: EDGE CASE
    """
    pass


def test_submit_joke_empty_text(client):
    """
    GIVEN ...
    WHEN ...
    THEN ...

    Level: ERROR CASE
    """
    pass


def test_submit_joke_over_max_length(client):
    """
    GIVEN ...
    WHEN ...
    THEN ...

    Level: EDGE CASE
    """
    pass


def test_submit_joke_whitespace_only(client):
    """
    GIVEN ...
    WHEN ...
    THEN ...

    Level: EDGE CASE
    """
    pass
