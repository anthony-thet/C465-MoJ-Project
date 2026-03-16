from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moj.db'

    db.init_app(app)
    migrate = Migrate(app, db)          # wires Flask-Migrate

    from app.routes.jokes import jokes_bp
    app.register_blueprint(jokes_bp)

    return app
