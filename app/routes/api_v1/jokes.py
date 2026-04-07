from flask import jsonify
from . import api_v1_bp


@api_v1_bp.route('/jokes/count', methods=['GET'])
def get_joke_count():
    try:
        count = Joke.query.count()
        response = jsonify({"data": {"count": count}, "status": "ok"})
        current_app.logger.info("Joke count requested", extra={
            "event": "joke_count_requested", "count": count,
            "endpoint": "GET /api/v1/jokes/count", "status_code": 200
        })
        return response, 200
    except Exception as e:
        return jsonify({
            "error": {"code": "INTERNAL_ERROR", "message": "Unable to retrieve joke count."}
        }), 500
