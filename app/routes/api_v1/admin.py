from functools import wraps
from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from app.models import Joke, User, db

admin_bp = Blueprint('api_v1_admin', __name__, url_prefix='/api/v1/admin')


def admin_required(f):
    """Decorator: requires authenticated user with role == 'admin'.
    Composes on @login_required — unauthenticated requests get 401,
    authenticated non-admins get 403. This is the Reference Monitor."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if current_user.role != 'admin':
            return jsonify({
                "error": {
                    "code": "FORBIDDEN",
                    "message": "Admin access required."
                }
            }), 403
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route('/jokes', methods=['GET'])
@admin_required
def admin_get_jokes():
    flagged_filter = request.args.get('flagged')
    query = Joke.query
    if flagged_filter == 'true':
        query = query.filter_by(flagged=True)
    jokes = query.all()
    return jsonify({
        "data": {
            "jokes": [
                {"id": j.id, "text": j.text, "author": j.author.username,
                 "flagged": j.flagged, "ai_rating": j.ai_rating}
                for j in jokes
            ]
        },
        "status": "ok"
    }), 200


@admin_bp.route('/jokes/<int:joke_id>', methods=['DELETE'])
@admin_required
def admin_delete_joke(joke_id):
    joke = Joke.query.get(joke_id)
    if not joke:
        return jsonify({
            "error": {"code": "NOT_FOUND", "message": "Joke not found."}
        }), 404
    db.session.delete(joke)
    db.session.commit()
    return '', 204


@admin_bp.route('/jokes/<int:joke_id>/flag', methods=['PATCH'])
@admin_required
def admin_flag_joke(joke_id):
    joke = Joke.query.get(joke_id)
    if not joke:
        return jsonify({
            "error": {"code": "NOT_FOUND", "message": "Joke not found."}
        }), 404
    data = request.get_json()
    if data is None or 'flagged' not in data:
        return jsonify({
            "error": {"code": "VALIDATION_ERROR",
                       "message": "Request must include 'flagged' field."}
        }), 422
    joke.flagged = bool(data['flagged'])
    db.session.commit()
    return jsonify({
        "data": {"joke": {"id": joke.id, "flagged": joke.flagged}},
        "status": "ok"
    }), 200


@admin_bp.route('/users', methods=['GET'])
@admin_required
def admin_get_users():
    users = User.query.all()
    return jsonify({
        "data": {
            "users": [
                {"id": u.id, "username": u.username, "role": u.role,
                 "joke_count": Joke.query.filter_by(user_id=u.id).count()}
                for u in users
            ]
        },
        "status": "ok"
    }), 200


@admin_bp.route('/users/<int:user_id>/role', methods=['PATCH'])
@admin_required
def admin_update_role(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            "error": {"code": "NOT_FOUND", "message": "User not found."}
        }), 404
    data = request.get_json()
    new_role = data.get('role') if data else None
    if new_role not in ('user', 'admin'):
        return jsonify({
            "error": {"code": "VALIDATION_ERROR",
                       "message": "Role must be 'user' or 'admin'."}
        }), 422
    user.role = new_role
    db.session.commit()
    return jsonify({
        "data": {"user": {"id": user.id, "username": user.username, "role": user.role}},
        "status": "ok"
    }), 200
