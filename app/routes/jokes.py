from flask import Blueprint, jsonify, request

jokes_bp = Blueprint('jokes', __name__)

_jokes = []


@jokes_bp.route('/jokes', methods=['GET'])
def get_jokes():
    return jsonify({"data": {"jokes": _jokes}, "status": "ok"}), 200


@jokes_bp.route('/jokes', methods=['POST'])
def post_joke():
    body = request.get_json(silent=True)
    text = body.get('text')

    if not body or not text:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "The 'text' field is required."
            }
        }), 400


    if text != "" and text.strip() == "":
        return jsonify({
            "error": {
                "code": "BAD_REQUEST",
                "message": "Text field cannot be only whitespace."
            }
        }), 400

    _jokes.append(text)

    if len(text) == 500:
        joke = {"text": body['text']}
        _jokes.append(joke)
        return jsonify({"data": joke, "status": "created"}), 201

    joke = {"text": body['text']}
    _jokes.append(joke)
    return jsonify({"data": joke, "status": "ok"}), 201
