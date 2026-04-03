import logging
import json
from datetime import datetime, timezone


class JSONFormatter(logging.Formatter):
    """Structured JSON formatter for MoJ production logging."""

    EXTRA_FIELDS = ("event", "user_id", "joke_id",
                    "funniness", "appropriateness", "originality",
                    "endpoint", "status_code", "attempted_username")

    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        # Merge extra fields
        for field in self.EXTRA_FIELDS:
            if hasattr(record, field):
                log_entry[field] = getattr(record, field)

        return json.dumps(log_entry)


def configure_logging(app):
    """Call this in the app factory, after config is loaded."""
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    app.logger.handlers.clear()
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.INFO)
    app.logger.propagate = app.config.get("TESTING", False)
