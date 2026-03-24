<<<<<<< HEAD
import pytest 
# from app import create_app
# from app.models import db as _db

# @pytest.fixture(scope='function')
# def app():
#     application = create_app(TestConfig)
#     with application.app_context():
#         _db.create_all()
#         yield application
#         _db.drop_all()

# @pytest.fixture(scope='function')
# def client(app):
#     return app.test_client()
=======
import pytest
from app import create_app
from app.models import db as _db


class TestConfig:
    TESTING = True


@pytest.fixture(scope='function')
def app():
    application = create_app(TestConfig)
    with application.app_context():
        _db.create_all()
        yield application
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()
>>>>>>> f4275708a7256af1fc80f57f38669f048d24c804
