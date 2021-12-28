from sqlalchemy import Table, Column, String, Integer, JSON
from sqlalchemy import ForeignKey
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

engine = create_engine("sqlite:///:memory:", echo=True)
base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class User(base):
    __tablename__ = "user_account"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String(50))
    email = Column(String(50), nullable=False)
    password = Column(String(30), nullable=False)

    credentials = relationship("Credential", back_populates="user")

    def __repr__(self):
        return f"User({self.name})"


class Credential(base):
    __tablename__ = "credential"

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey("user_account.id"), nullable=False)
    website = Column(String(50), nullable=True)
    keys_values = Column(JSON, nullable=True)

    user = relationship("User", back_populates="credentials")
    shared_users = relationship("Sharing", back_populates="credential")

    def __repr__(self):
        return f"Credentials({self.keys_values!r})"


class Sharing(base):
    __tablename__ = "sharing"

    id = Column(Integer, primary_key=True)
    credential_id = Column(ForeignKey("credential.id"), nullable=False)
    shared_user_id = Column(ForeignKey("user_account.id"), nullable=False)

    credential = relationship("Credential", back_populates="shared_users")


base.metadata.create_all(engine)
