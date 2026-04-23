import pytest
from app.models import Joke, db


class TestJokeCountEndpoint:
    """Tests for GET /api/v1/jokes/count"""
    def test_joke_count_returns_200(self, client):
        """
        GIVEN an application with the API v1 blueprint registered
        WHEN the client sends GET /api/v1/jokes/count
        THEN the response status code should be 200
        Level: HAPPY PATH
        """
        response = client.get('/api/v1/jokes/count')
        assert response.status_code == 200

    def test_joke_count_returns_envelope(self, client):
        """
        GIVEN an application with jokes in the database
        WHEN the client sends GET /api/v1/jokes/count
        THEN the response body should contain 'data' with an
        integer 'count' and 'status' == 'ok'
        Level: HAPPY PATH
        """
        response = client.get('/api/v1/jokes/count')
        body = response.get_json()
        assert body["status"] == "ok"
        assert "count" in body["data"]
        assert isinstance(body["data"]["count"], int)

    def test_joke_count_zero_when_empty(self, client):
        """
        GIVEN a database with no jokes
        WHEN the client sends GET /api/v1/jokes/count
        THEN the count returned should be 0
        Level: EDGE CASE
        """
        # Logic assumes a fresh test database or session cleanup
        response = client.get('/api/v1/jokes/count')
        body = response.get_json()
        assert body["data"]["count"] == 0

    def test_joke_count_wrong_method_returns_405(self, client):
        """
        GIVEN the joke count endpoint
        WHEN the client sends a POST request instead of GET
        THEN the response status code should be 405 and return the error envelope
        Level: ERROR CASE
        """
        response = client.post('/api/v1/jokes/count')
        body = response.get_json()
        assert response.status_code == 405
        assert body["error"]["code"] == "METHOD_NOT_ALLOWED"


class TestJokesListEndpoint:
    @pytest.fixture(autouse=True)
    def ensure_submission(self, authenticated_client, app):
        """
        Ensure the authenticated user has submitted a joke
        to satisfy the 'Leave a penny, take a penny' requirement.
        """
        with app.app_context():
            # current_user.id in the session is 1 for the first test user
            if not Joke.query.filter_by(submitted_by=1).first():
                joke = Joke(text="Test setup joke", submitted_by=1)
                db.session.add(joke)
                db.session.commit()

    def test_get_jokes_returns_200(self, authenticated_client):
        """
        GIVEN an application with the API v1 blueprint registered
        WHEN the client sends GET /api/v1/jokes
        THEN the response status code should be 200

        Level: HAPPY PATH
        """
        response = authenticated_client.get('/api/v1/jokes')
        assert response.status_code == 200

    def test_get_jokes_returns_envelope(self, authenticated_client):
        """
        GIVEN an application with jokes in the database
        WHEN the client sends GET /api/v1/jokes
        THEN the response body should contain 'data.jokes' as a list
             and 'status' == 'ok'

        Level: HAPPY PATH
        """
        response = authenticated_client.get('/api/v1/jokes')
        body = response.get_json()
        assert body["status"] == "ok"
        assert isinstance(body["data"]["jokes"], list)

    def test_get_jokes_fields_are_filtered(self, authenticated_client, sample_joke):
        """
        GIVEN a joke exists in the database
        WHEN the client sends GET /api/v1/jokes
        THEN each joke object should contain only 'id', 'text', 'author', 'ai_rating'
             — no 'user_id', 'created_at', or other internal fields

        Level: EDGE CASE
        """
        response = authenticated_client.get('/api/v1/jokes')
        body = response.get_json()
        joke = body["data"]["jokes"][0]
        assert set(joke.keys()) == {"id", "text", "author", "ai_rating"}

    def test_get_jokes_wrong_method_returns_405(self, client):
        """
        GIVEN the API v1 blueprint is registered
        WHEN the client sends DELETE /api/v1/jokes
        THEN the response status code should be 405

        Level: ERROR CASE
        """
        response = client.delete('/api/v1/jokes')
        assert response.status_code == 405

    def test_get_jokes_requires_auth(self, client):
        """
        GIVEN an unauthenticated client
        WHEN the client sends GET /api/v1/jokes without a session
        THEN the response should be 401 UNAUTHORIZED

        Level: ERROR CASE
        """
        with client.session_transaction() as session:
            session.clear()

        response = client.get('/api/v1/jokes')
        assert response.status_code == 401
