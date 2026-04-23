from flask import jsonify, current_app
from flask_login import login_required, current_user
import re
import requests
from app.models import Joke
from . import api_v1_bp


def parse_rating(text: str) -> int | None:
    """Extract the first integer 1–10 from an LLM response string.
    Returns None if no valid rating found."""
    match = re.search(r'\b(10|[1-9])\b', text.strip())
    return int(match.group(1)) if match else None


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
@login_required
def get_jokes():
    has_submitted = Joke.query.filter_by(submitted_by=current_user.id).count() > 0
    if not has_submitted:
        return jsonify({
            "error": {
                "code": "HAS_NOT_SUBMITTED",
                "message": "Submit a joke before browsing. Leave a penny, take a penny."
            }
        }), 403
    """Return all jokes with only the fields the frontend needs."""
    try:
        jokes = Joke.query.filter_by(flagged=False).all()
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
                        "author": joke.author.username,
                        "ai_rating": joke.ai_rating
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


@api_v1_bp.route('/jokes/<int:joke_id>/rate', methods=['POST'])
@login_required
def rate_joke(joke_id):
    joke = Joke.query.get_or_404(joke_id)
    prompt = (
        f"Rate this joke from 1 to 10, where 1 is not funny and 10 is hilarious. "
        f"Respond with only a single integer. Joke: {joke.text}"
    )
    try:
        resp = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": "llama3.2:1b", "prompt": prompt, "stream": False},
            timeout=30,
        )
        resp.raise_for_status()
        rating = parse_rating(resp.json().get('response', ''))
    except requests.exceptions.RequestException:
        return jsonify({
            "error": {"code": "OLLAMA_UNAVAILABLE",
                      "message": "AI rating service is unavailable."}
        }), 503
    joke.ai_rating = rating
    db.session.commit()
    return jsonify({
        "data": {"joke_id": joke.id, "ai_rating": joke.ai_rating},
        "status": "ok"
    }), 200
