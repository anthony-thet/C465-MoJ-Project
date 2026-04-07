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
        THEN the response body should contain 'data' with an integer 'count' and 'status' == 'ok'

        Level: HAPPY PATH
        """
        response = client.get('/api/v1/jokes/count')
        body = response.get_json()
        assert body["status"] == "ok"
        assert isinstance(body["data"]["count"], int)
