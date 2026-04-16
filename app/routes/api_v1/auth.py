from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, db, Joke

api_v1_auth_bp = Blueprint('api_v1_auth', __name__, url_prefix='/api/v1/auth')


@api_v1_auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            "error": {"code": "VALIDATION_ERROR",
                      "message": "Username and password are required."}
        }), 422

    # Check for existing user
    if User.query.filter_by(username=data['username']).first():
        return jsonify({
            "error": {"code": "CONFLICT",
                      "message": "Username already taken."}
        }), 409

    user = User(username=data['username'])
    user.set_password(data['password'])

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "data": {"user": {"id": user.id, "username": user.username, "role": user.role}},
        "status": "ok"
    }), 201


@api_v1_auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('username') or not data.get('password'):
        return jsonify({
            "error": {"code": "VALIDATION_ERROR",
                      "message": "Username and password are required."}
        }), 422

    user = User.query.filter_by(username=data['username']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({
            "error": {"code": "UNAUTHORIZED",
                      "message": "Invalid username or password."}
        }), 401

    login_user(user)

    return jsonify({
        "data": {"user": {"id": user.id, "username": user.username, "role": user.role}},
        "status": "ok"
    }), 200


@api_v1_auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"data": {}, "status": "ok"}), 200


@api_v1_auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    has_submitted = Joke.query.filter_by(user_id=current_user.id).count() > 0
    return jsonify({
        "data": {
            "user": {
                "id": current_user.id,
                "username": current_user.username,
                "role": current_user.role,
                "has_submitted": has_submitted
            }
        },
        "status": "ok"
    }), 200