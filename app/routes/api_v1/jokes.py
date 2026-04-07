from flask import jsonify
from . import api_v1_bp


@api_v1_bp.route('/jokes/count', methods=['GET'])
def get_joke_count():
    count = Joke.query.count()
    return jsonify({
        "data": {"count": count},
        "status": "ok"
    }), 200
