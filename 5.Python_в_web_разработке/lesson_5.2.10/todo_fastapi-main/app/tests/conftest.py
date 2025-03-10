import os
from typing import Generator, NamedTuple

import pytest
from alembic.command import downgrade, upgrade
from alembic.config import Config

from .api_client import TodoApiClient
from .config import API_HOST
from .constants import (
    ADMIN_PASSWORD,
    DEFAULT_USER_NAME,
    DEFAULT_USER_PASSWORD,
    NEW_TODO_ITEM_IMPORTANT,
    NEW_TODO_ITEM_NOT_IMPORTANT,
    NEW_USER_NAME,
    NEW_USER_NAME_WITH_TODOS,
)


class NewUser(NamedTuple):
    client: TodoApiClient
    id: int


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "alembic.ini")

    downgrade(Config(config_path), "base")
    upgrade(Config(config_path), "head")


@pytest.fixture()
def client():
    return TodoApiClient(API_HOST)


@pytest.fixture()
def admin_client():
    client = TodoApiClient(API_HOST)
    client.auth("admin", ADMIN_PASSWORD)
    return client


@pytest.fixture(scope="session")
def user_client():
    client = TodoApiClient(API_HOST)
    client.create_user(DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD)
    client.auth(DEFAULT_USER_NAME, DEFAULT_USER_PASSWORD)
    return client


@pytest.fixture()
def client_without_auth():
    client = TodoApiClient(API_HOST)
    client.headers = {"x-token": "6c61502f-32c6-4b22-b370-b64bc28920e2"}
    return client


@pytest.fixture()
def new_user(client: TodoApiClient) -> Generator[NewUser, None, None]:
    response = client.create_user(NEW_USER_NAME, DEFAULT_USER_PASSWORD)
    client.auth(NEW_USER_NAME, DEFAULT_USER_PASSWORD)
    yield NewUser(client, response.id)
    client.delete_user(response.id)


@pytest.fixture()
def new_user_with_todos(client: TodoApiClient) -> Generator[NewUser, None, None]:
    response = client.create_user(NEW_USER_NAME_WITH_TODOS, DEFAULT_USER_PASSWORD)
    client.auth(NEW_USER_NAME_WITH_TODOS, DEFAULT_USER_PASSWORD)
    client.create_todo(NEW_TODO_ITEM_IMPORTANT, True)
    client.create_todo(NEW_TODO_ITEM_NOT_IMPORTANT, False)
    yield NewUser(client, response.id)
    client.delete_user(response.id)
