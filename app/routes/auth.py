from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    user = User(username=username)

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({'username': user.username}), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(username=data.get('username')).first()

    if user is None or not user.check_password(data.get('password', '')):
        return jsonify({'error': 'Invalid credentials'}), 401

    login_user(user)

    return jsonify({'message': f'Welcome, {user.username}'}), 200


@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'}), 200


@auth_bp.route('/admin/users', methods=['GET'])
@login_required
def list_users():
    if current_user.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    users = User.query.all()

    return jsonify([
        {'id': u.id, 'username': u.username, 'role': u.role}
        for u in users
    ]), 200
