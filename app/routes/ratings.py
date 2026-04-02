from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Rating
from app.models import Joke

ratings_bp = Blueprint('ratings', __name__)


def validate_rating_data(data):
    "Helper to validate axes are integers 1-5"
    axes = ['funniness', 'appropriateness', 'originality']
    for axis in axes:
        val = data.get(axis)
        if not isinstance(val, int) or not (1 <= val <= 5):
            return f"{axis} must be an integer between 1 and 5"
    return None


@ratings_bp.route('/jokes/<int:joke_id>/ratings', methods=['POST'])
@login_required
def create_rating(joke_id):
    """Create a new rating for a joke. Non-idempotent — use PUT to update."""
    Joke.query.get_or_404(joke_id)

    data = request.get_json() or {}
    error_msg = validate_rating_data(data)
    if error_msg:
        return jsonify({
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": error_msg
                }
            }), 400

    existing = Rating.query.filter_by(user_id=current_user.id, joke_id=joke_id).first()
    if existing:
        return jsonify({
                "error": {
                    "code": "DUPLICATE_RATING",
                    "message": "This joke has already been rated"
                }
            }), 409

    new_rating = Rating(
        user_id=current_user.id,
        joke_id=joke_id,
        funniness=data['funniness'],
        appropriateness=data['appropriateness'],
        originality=data['originality']
    )
    db.session.add(new_rating)
    db.session.commit()

    return jsonify({
        "data": {
            "id": new_rating.id,
            "user_id": new_rating.user_id,
            "joke_id": new_rating.joke_id,
            "funniness": new_rating.funniness,
            "appropriateness": new_rating.appropriateness,
            "originality": new_rating.originality,
            "created_at": new_rating.created_at,
            "updated_at": new_rating.updated_at
        },
        "status": "ok"
    }), 201


@ratings_bp.route('/jokes/<int:joke_id>/ratings/me', methods=['GET'])
@login_required
def get_my_rating(joke_id):
    rating = Rating.query.filter_by(user_id=current_user.id, joke_id=joke_id).first()
    if not rating:
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "Rating not found."
            }
        }), 404

    return jsonify({
        "data": {
            "id": rating.id,
            "user_id": rating.user_id,
            "joke_id": rating.joke_id,
            "funniness": rating.funniness,
            "appropriateness": rating.appropriateness,
            "originality": rating.originality,
            "created_at": rating.created_at,
            "updated_at": rating.updated_at
        },
        "status": "ok"
    }), 200


@ratings_bp.route('/jokes/<int:joke_id>/ratings/me', methods=['PUT'])
@login_required
def update_my_rating(joke_id):
    """Update the current user's rating. Idempotent — safe to retry."""
    rating = Rating.query.filter_by(user_id=current_user.id, joke_id=joke_id).first()
    if not rating:
        return jsonify({
            "error": {
                "code": "NOT_FOUND",
                "message": "Rating not found."
            }
        }), 404

    data = request.get_json() or {}
    error_msg = validate_rating_data(data)
    if error_msg:
        return jsonify({
            "error": {
                "code": "VALIDATION_ERROR",
                "message": error_msg
            }
        }), 400

    rating.funniness = data['funniness']
    rating.appropriateness = data['appropriateness']
    rating.originality = data['originality']

    db.session.commit()

    return jsonify({
        "data": {
            "id": rating.id,
            "user_id": rating.user_id,
            "joke_id": rating.joke_id,
            "funniness": rating.funniness,
            "appropriateness": rating.appropriateness,
            "originality": rating.originality,
            "created_at": rating.created_at,
            "updated_at": rating.updated_at
        },
        "status": "ok"
    }), 200
