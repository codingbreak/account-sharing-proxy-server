import pytest

from database import db
from init import create_app


@pytest.fixture(autouse=True)
def test_app():
    app = create_app()
    yield app

    db.drop_all()


@pytest.fixture(autouse=True)
def session():
    # Setup database
    db.create_all()

    yield db.session

    # Clear data after each test
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()
