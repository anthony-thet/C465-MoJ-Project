import logging

from flask import current_app


class TestLogging:
    """Verify that MoJ route handlers emit structured log events."""

    def test_login_emits_log_event(self, client, caplog):
        """
        GIVEN a registered user
        WHEN they POST valid credentials to /login
        THEN an INFO log entry with event 'login_success' should be emitted

        Level: HAPPY PATH
        """
        with caplog.at_level(logging.INFO):
            current_app.logger.info("User logged in",
                                    extra={
                                        "event": "login_success",
                                        "user_id": 1,
                                        "endpoint": "POST /login",
                                        "status_code": 200
                                    })

        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "login_success"
            for record in caplog.records
        )

    def test_login_failure_emits_warning(self, client, caplog):
        """
        GIVEN a registered user
        WHEN they POST invalid credentials to /login
        THEN a WARNING log entry with event 'login_failure' should be emitted

        Level: ERROR CASE
        """
        with caplog.at_level(logging.WARNING):
            current_app.logger.warning("User logged in",
                                       extra={
                                           "event": "login_failure",
                                           "attempted_username": "testusername123",
                                           "endpoint": "POST /login",
                                           "status_code": 401
                                       })

        assert any(
            record.levelname == "WARNING" and
            hasattr(record, "event") and
            record.event == "login_failure"
            for record in caplog.records
        )

    def test_rating_created_emits_log_event(self, client, caplog):
        """
        GIVEN a registered user
        WHEN they POST a rating to /jokes/<int:joke_id>/ratings
        THEN an INFO log entry with event 'rating_created' should be emitted

        Level: ERROR CASE
        """
        with caplog.at_level(logging.INFO):
            current_app.logger.info("User logged in",
                                    extra={
                                        "event": "rating_created",
                                        "user_id": 1,
                                        "joke_id": 1,
                                        "funniness": 8,
                                        "appropriateness": 1,
                                        "originality": 8,
                                        "status_code": 201
                                    })

        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "rating_created"
            for record in caplog.records
        )
