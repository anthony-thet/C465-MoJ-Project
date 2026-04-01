# from app import db
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    jokes = db.relationship('Joke', backref='author', lazy=True)
    role = db.Column(db.String(20), default='joke-teller')

    def __repr__(self):
        return f'<User {self.username}>'

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Joke(db.Model):
    __tablename__ = 'joke'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=False)
    submitted_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f'<Joke {self.id}>'


class Rating(db.Model):
    __tablename__ = 'ratings'

    id              = db.Column(db.Integer, primary_key=True)
    user_id         = db.Column(db.Integer, db.ForeignKey('users.id'),
                                nullable=False)
    joke_id         = db.Column(db.Integer, db.ForeignKey('jokes.id'),
                                nullable=False)
    funniness       = db.Column(db.Integer, nullable=False)
    appropriateness = db.Column(db.Integer, nullable=False)
    originality     = db.Column(db.Integer, nullable=False)
    created_at      = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at      = db.Column(db.DateTime, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'joke_id',
                            name='one_rating_per_user_per_joke'),
    )
