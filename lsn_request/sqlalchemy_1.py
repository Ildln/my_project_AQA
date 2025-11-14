import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, Column, Integer, String

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)

@pytest.fixture(scope="session")
def db_engine():
    engine = create_engine("postgresql://user:password@localhost:5432/test_db")
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(de_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()

def test_user_saved_in_db(db_engine):

    user = User(name="TestUser", age=22)
    db_session.add(user)
    db_session.commit()

    result = db_session.query(User).filter_by(name="TestUser").first()
    assert result is not None
    assert result.age == 22