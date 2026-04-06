from flask import Blueprint, jsonify, request, current_app

jokes_bp = Blueprint('jokes', __name__)

_jokes = []
_next_id = 1


@jokes_bp.route('/jokes', methods=['GET'])
def get_jokes():
    return jsonify({"data": {"jokes": _jokes}, "status": "ok"}), 200


@jokes_bp.route('/jokes', methods=['POST'])
def post_joke():
    body = request.get_json(silent=True)
    text = body.get('text')

    user_id = None

    if body.get('user_id'):
        user_id = body.get('user_id')

    if not body or not text:
        return jsonify({
            "status": "error",
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The 'text' field is required."
            }
        }), 400

    if len(text) > 500:
        return jsonify({
            "error": {
                "code": "USER_ERROR",
                "message": "The 'text' field is too long"
            }
        }), 400

    if text != "" and text.strip() == "":
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Text field cannot be only whitespace."
            }
        }), 400

    if len(text) == 500:
        joke = {"text": body['text']}
        _jokes.append(joke)
        return jsonify({"data": joke, "status": "created"}), 201

    global _next_id
    new_joke = {
        "id": _next_id,
        "text": text
    }
    _jokes.append(new_joke)
    _next_id += 1

    current_app.logger.info(
        "Joke created",
        extra={
            "event": "joke_created",
            "user_id": user_id,
            "joke_id": new_joke['id'],
            "endpoint": "POST /jokes",
            "status_code": 201
        }
    )

    return jsonify({"data": new_joke, "status": "ok"}), 201
