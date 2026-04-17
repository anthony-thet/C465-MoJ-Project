from flask import Flask, jsonify
from flask_migrate import Migrate
from app.models import db
from flask_login import LoginManager
from app.models import User
from app.utils.logging_config import configure_logging
from flask_cors import CORS
login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)
    CORS(app,
         origins=["http://localhost:5173"],
         supports_credentials=True,
         allow_headers=["Content-Type"],
         methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"])

    if config is not None:
        app.config.from_object(config)

    configure_logging(app)

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)          # wires Flask-Migrate

    from app.routes.jokes import jokes_bp
    app.register_blueprint(jokes_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.ratings import ratings_bp
    app.register_blueprint(ratings_bp)

    from app.routes.api_v1 import api_v1_bp
    app.register_blueprint(api_v1_bp)

    from routes.api_v1.auth import api_v1_auth_bp
    app.register_blueprint(api_v1_auth_bp)

    return app


@login_manager.user_loader
def load_user(user_id):
    """Called on every request with a valid session cookie.
    Returns the User object, or None if the session is invalid."""
    return User.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({
        "error": {
            "code": "UNAUTHORIZED",
            "message": "Authentication required."
        }
    }), 401
