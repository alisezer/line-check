# from flask.testing import FlaskClient
import pytest

from lc.main import create_app, db

@pytest.fixture
def test_client():
    flask_app = create_app()
    with flask_app.test_client() as test_client:
        with flask_app.app_context():
            yield test_client


@pytest.fixture
def test_db():
    flask_app = create_app()
    with flask_app.app_context():
        db.drop_all()
        db.create_all()
    yield db