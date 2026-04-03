import logging


class TestLogging:
    """Verify that MoJ route handlers emit structured log events."""

    def test_login_emits_log_event(self, client, sample_user, caplog):
        """
        GIVEN a registered user
        WHEN they POST valid credentials to /login
        THEN an INFO log entry with event 'login_success' should be emitted

        Level: HAPPY PATH
        """
        with caplog.at_level(logging.INFO):
            response = client.post('/login', json={
                'username': 'qauser',
                'password': 'testpass'
            })

        assert response.status_code == 200
        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "login_success"
            for record in caplog.records
        )

    def test_login_failure_emits_warning(self, client, sample_user, caplog):
        """
        GIVEN a registered user
        WHEN they POST invalid credentials to /login
        THEN a WARNING log entry with event 'login_failure' should be emitted

        Level: ERROR CASE
        """
        with caplog.at_level(logging.WARNING):
            response = client.post('/login', json={
                'username': 'qauser',
                'password': 'wrongtestpass'
            },
                                   )
        assert response.status_code == 401
        assert any(
            record.levelname == "WARNING" and
            hasattr(record, "event") and
            record.event == "login_failure"
            for record in caplog.records
        )

    def test_rating_created_emits_log_event(self, authenticated_client,
                                            caplog, sample_joke):
        """
        GIVEN a registered user and an existing joke
        WHEN they POST a valid rating to /jokes/<int:joke_id>/ratings
        THEN an INFO log entry with event 'rating_created' should be emitted

        Level: HAPPY PATH
        """
        with caplog.at_level(logging.INFO):
            response = authenticated_client.post(
                f'/jokes/{sample_joke.id}/ratings',
                json={
                    "funniness": 4,
                    "appropriateness": 5,
                    "originality": 3
                })

        assert response.status_code == 201
        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "rating_created"
            for record in caplog.records
        )
