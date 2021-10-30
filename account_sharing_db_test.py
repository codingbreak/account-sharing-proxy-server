from sqlalchemy import insert, select, bindparam
from account_sharing_db import *
import pytest


@pytest.fixture
def session():
    from sqlalchemy import MetaData, create_engine
    from sqlalchemy.orm import sessionmaker
    
    engine = create_engine('sqlite:///:memory:', echo=True)	
    base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    yield session


def test_create_user_account(session):
    new_user = User(name="a_name", fullname="a_fulname", email="an_email@host")
    session.add(new_user)
