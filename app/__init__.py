from flask import Flask
from flask_migrate import Migrate
from app.models import db
from flask_login import LoginManager
from app.models import User
import rating

login_manager = LoginManager()


def create_app(config=None):
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moj.db'

    db.init_app(app)
    login_manager.init_app(app)
    Migrate(app, db)          # wires Flask-Migrate

    from app.routes.jokes import jokes_bp
    app.register_blueprint(jokes_bp)

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from app.routes.rating import ratings_bp
    app.register_blueprint(ratings_bp)
    
    return app


@login_manager.user_loader
def load_user(user_id):
    """Called on every request with a valid session cookie.
    Returns the User object, or None if the session is invalid."""
    return User.query.get(int(user_id))
