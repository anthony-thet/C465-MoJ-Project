from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Rating
from models import Joke

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
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": error_msg}}), 400

    existing = Rating.query.filter_by(user_id=current_user.id, joke_id=joke_id).first()
    if existing:
        return jsonify({"error": {"code": "DUPLICATE_RATING", "message": "This joke has already been rated"}}), 409

    new_rating = Rating(
        user_id = current_user.id,
        joke_id = joke_id,
        selected_scores = {}
        for k in ['funniness', 'appropriateness', 'originality']:
            selected_scores[k] = data[k]
    )
    db.session.add(new_rating)
    db.session.commit()
    return jsonify(new_rating.to_dict()), 201
    # TODO: Implement
    #   2. Validate all three axes are present and integers 1-5 (400 if not)
    #   3. Check for duplicate rating by this user on this joke (409 if exists)
    #   4. Create and save the Rating
    #   5. Return 201 with the rating data
    pass


@ratings_bp.route('/jokes/<int:joke_id>/ratings/me', methods=['GET'])
@login_required
def get_my_rating(joke_id):
    """Get the current user's rating for a joke."""
    # TODO: Implement
    #   1. Query for rating by current_user.id and joke_id
    #   2. Return 200 with rating data, or 404 if no rating exists
    pass


@ratings_bp.route('/jokes/<int:joke_id>/ratings/me', methods=['PUT'])
@login_required
def update_my_rating(joke_id):
    """Update the current user's rating. Idempotent — safe to retry."""
    # TODO: Implement
    #   1. Find existing rating (404 if none)
    #   2. Validate new scores (same rules as POST)
    #   3. Update the fields and commit
    #   4. Return 200 with updated rating data
    pass
