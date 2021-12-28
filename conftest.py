import pytest

from database import db
from init import create_app


@pytest.fixture(autouse=True)
def test_app():
    app = create_app(site_name="https://reqbin.com/")
    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture(autouse=True)
def session(test_app):
    with test_app.app_context():
        # Setup database
        db.create_all()

        yield db.session

        # Clear data after each test
        meta = db.metadata
        for table in reversed(meta.sorted_tables):
            db.session.execute(table.delete())
        db.session.commit()


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        yield client
