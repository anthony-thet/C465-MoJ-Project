

def test_db_initializes(app):
    """
    GIVEN a configured Flask application
    WHEN the app context is active
    THEN the database should be accessible without error

    Level: HAPPY PATH
    """
    with app.app_context():
        from app.models import User, Joke
        assert User.__tablename__ == 'user'
        assert Joke.__tablename__ == 'joke'
