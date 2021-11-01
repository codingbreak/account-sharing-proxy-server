import pytest
from database import *


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


def test_create_user_account(session):
    guest = User(username="guest", email="guest@example.com")
    session.add(guest)
    session.commit()

    assert User.query.filter_by(username='guest').first() == guest


def test_create_credential(session):
    guest = User(username="guest", email="guest@example.com")
    guest_wsj_cre = Credential(website="https://www.wsj.com/",user=guest)
    session.add(guest)
    session.add(guest_wsj_cre)
    session.commit()

    assert Credential.query.filter_by(website="https://www.wsj.com/").first() == guest_wsj_cre


def test_share_credential(session):
    guest = User(username="guest", email="guest@example.com")
    guest_wsj_cre = Credential(website="https://www.wsj.com/",user=guest)
    session.add(guest)
    session.add(guest_wsj_cre)
    session.commit()

    guest_friend = User(username="guest_friend", email="guest_friend@example.com")
    guest_wsj_cre_to_guest_friend = Shared_User(credential=guest_wsj_cre, shared_user=guest_friend)
    session.add(guest_friend)
    session.add(guest_wsj_cre_to_guest_friend)
    session.commit()

    assert Shared_User.query.filter_by(shared_user=guest_friend).first().credential.user == guest

