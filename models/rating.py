from datetime import datetime
from app import db


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
