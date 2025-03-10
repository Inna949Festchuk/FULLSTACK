import datetime
import time
from dataclasses import dataclass

import pytest
import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tests.api import login
from config import PG_USER, PG_PASSWORD, PG_HOST, PG_PORT, PG_DB
from models import Base, User
from auth import hash_password
from tests.config import API_URL

engine = create_engine(f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}")
Session = sessionmaker(bind=engine)


@dataclass
class UserData:
    id: int
    name: str
    password: str
    creation_time: datetime.datetime


@pytest.fixture(scope="session", autouse=True)
def init_database():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


def create_user(name: str, password: str):
    with Session() as session:
        password = hash_password(password)
        new_user = User(name=name, password=password)
        session.add(new_user)
        session.commit()
        return UserData(id=new_user.id, name=name, password=password, creation_time=new_user.creation_time)


@pytest.fixture(scope="session", autouse=True)
def root_user():
    return create_user("root", "toor")


@pytest.fixture(scope="session", autouse=True)
def root_user_token():
    return login("root", "toor")["token"]


@pytest.fixture()
def new_user():
    name = f"new_user_{time.time()}"
    return create_user(name, "1234")
