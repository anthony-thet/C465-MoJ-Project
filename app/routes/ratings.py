from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from models.rating import Rating
from models.joke import Joke

ratings_bp = Blueprint('ratings', __name__)


@ratings_bp.route('/jokes/<int:joke_id>/ratings', methods=['POST'])
@login_required
def create_rating(joke_id):
    """Create a new rating for a joke. Non-idempotent — use PUT to update."""
    # TODO: Implement
    #   1. Verify the joke exists (404 if not)
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
