import logging


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
            # TODO: perform login via client
            pass

        assert any(
            record.levelname == "INFO" and
            hasattr(record, "event") and
            record.event == "login_success"
            for record in caplog.records
        )
