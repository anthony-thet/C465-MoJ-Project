from flask import Blueprint, jsonify, request

jokes_bp = Blueprint('jokes', __name__)

_jokes = []

@jokes_bp.route('/jokes', methods=['GET'])
def get_jokes():
    return jsonify({"data": {"jokes": _jokes}, "status": "ok"}), 200

@jokes_bp.route('/jokes', methods=['POST'])
def post_joke():
    body = request.get_json(silent=True)
    if not body or not body.get('text'):
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The 'text' field is required."
            }
        }), 400
    joke = {"text": body['text']}
    _jokes.append(joke)
    return jsonify({"data": joke, "status": "ok"}), 201
