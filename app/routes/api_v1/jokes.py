from flask import jsonify, current_app
from app.models import Joke
from . import api_v1_bp


@api_v1_bp.route('/jokes/count', methods=['GET'])
def get_joke_count():
    try:
        count = Joke.query.count()

        # Log the event (current_app is now imported)
        current_app.logger.info("Joke count requested", extra={
            "event": "joke_count_requested",
            "count": count,
            "endpoint": "GET /api/v1/jokes/count",
            "status_code": 200
        })

        return jsonify({
            "data": {"count": count},
            "status": "ok"
        }), 200

    except Exception as e:
        current_app.logger.error(f"API Error: {str(e)}")
        return jsonify({
            "status": "error",
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Unable to retrieve joke count."
            }
        }), 500


@api_v1_bp.app_errorhandler(404)
def not_found(e):
    return jsonify({
        "error": {
            "code": "NOT_FOUND",
            "message": "The requested resource does not exist."
        }
    }), 404


@api_v1_bp.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({
        "error": {
            "code": "METHOD_NOT_ALLOWED",
            "message": "This HTTP method is not supported for this endpoint."
        }
    }), 405


@api_v1_bp.route('/jokes', methods=['GET'])
def get_jokes():
    """Return all jokes with only the fields the frontend needs."""
    try:
        jokes = Joke.query.all()
        current_app.logger.info(
            "Jokes list requested",
            extra={
                "event": "jokes_list_requested",
                "count": len(jokes),
                "endpoint": "GET /api/v1/jokes",
                "status_code": 200
            })
        
        return jsonify({
            "data": {
                "jokes": [
                    {
                        "id": joke.id,
                        "text": joke.text,
                        "author": joke.author.username
                            if joke.author else "anonymous"
                    }
                    for joke in jokes
                ]
            },
            "status": "ok"
        }), 200
    except Exception:
        return jsonify({
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Unable to retrieve jokes."
            }
        }), 500
