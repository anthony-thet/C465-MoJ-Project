class TestAuthEndpoint:
    def test_register_success(self, client):
        """
        GIVEN an application with the auth blueprint registered
        WHEN the client POSTs valid username and password to /api/v1/auth/register
        THEN the response should be 201 with the new user in the envelope

        Level: HAPPY PATH
        """
        response = client.post('/api/v1/auth/register',
                               json={'username': 'newuser', 'password': 'secret123'})
        assert response.status_code == 201
        body = response.get_json()
        assert body['data']['user']['username'] == 'newuser'

    def test_register_duplicate_username(self, client, sample_user):
        """
        GIVEN a user 'alice' already exists
        WHEN the client POSTs username 'alice' to /api/v1/auth/register
        THEN the response should be 409 CONFLICT

        Level: ERROR CASE
        """
        response = client.post('/api/v1/auth/register',
                               json={'username': 'qauser', 'password': 'secret123'})
        assert response.status_code == 409
        assert response.get_json()['error']['code'] == 'CONFLICT'

    def test_login_success(self, client, sample_user):
        """
        GIVEN a user 'alice' exists with password 'correctpassword'
        WHEN the client POSTs valid credentials to /api/v1/auth/login
        THEN the response should be 200 with the user in the envelope

        Level: HAPPY PATH
        """
        response = client.post('/api/v1/auth/login',
                               json={'username': 'qauser', 'password': 'testpass'})
        assert response.status_code == 200
        assert response.get_json()['data']['user']['username'] == 'qauser'

    def test_login_wrong_password(self, client, sample_user):
        """
        GIVEN a user 'alice' exists
        WHEN the client POSTs an incorrect password to /api/v1/auth/login
        THEN the response should be 401 UNAUTHORIZED

        Level: ERROR CASE
        """
        response = client.post('/api/v1/auth/login',
                               json={'username': 'qauser', 'password': 'wrongpassword'})
        assert response.status_code == 401
        assert response.get_json()['error']['code'] == 'UNAUTHORIZED'
