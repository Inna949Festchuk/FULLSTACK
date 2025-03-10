import uuid

import requests
import pytest

from tests.config import API_URL
from tests import api


DEFAULT_PASSWORD = "1234"


def test_root():
    response = requests.get(API_URL)
    assert response.status_code == 404


class TestUser:
    def test_login(self, new_user):
        assert "token" in api.login(new_user.name, DEFAULT_PASSWORD)

    def test_bad_password(self, new_user):
        with pytest.raises(api.HttpError) as error:
            api.login(new_user.name, f"{DEFAULT_PASSWORD}!")
        assert error.value.status_code == 401
        assert error.value.message == {"status": "error", "description": "incorrect login or password"}

    def test_bad_username(self):
        with pytest.raises(api.HttpError) as error:
            api.login("some_none_existed", DEFAULT_PASSWORD)

        assert error.value.status_code == 401
        assert error.value.message == {"status": "error", "description": "incorrect login or password"}

    def test_get_user(self, root_user, root_user_token):

        user = api.get_user(root_user.id, root_user_token)
        assert user == {
            "id": root_user.id,
            "name": root_user.name,
            "creation_time": int(root_user.creation_time.timestamp()),
        }

    def test_get_user_bad_token(self, root_user):

        with pytest.raises(api.HttpError) as error:
            api.get_user(root_user.id, str(uuid.uuid4()))

        assert error.value.status_code == 403
        assert error.value.message == {"description": "incorrect token", "status": "error"}

    def test_get_user_non_existed(self, root_user_token):
        with pytest.raises(api.HttpError) as error:
            api.get_user(999, root_user_token)

        assert error.value.status_code == 404
        assert error.value.message == {"status": "error", "description": "User not found"}

    def test_get_user_non_existed_bad_token(self):
        with pytest.raises(api.HttpError) as error:
            api.get_user(999, str(uuid.uuid4()))

        assert error.value.status_code == 403
        assert error.value.message == {"description": "incorrect token", "status": "error"}

    def test_get_another_user(self, root_user_token, new_user):
        user = api.get_user(new_user.id, root_user_token)
        assert user == {
            "id": new_user.id,
            "name": new_user.name,
            "creation_time": int(new_user.creation_time.timestamp()),
        }

    def test_create_user(self, root_user_token):
        user_id = api.create_user("user_2", DEFAULT_PASSWORD)["id"]
        user = api.get_user(user_id, root_user_token)
        assert user["name"] == "user_2"

    def test_patch_user(self, new_user):
        token = api.login(new_user.name, DEFAULT_PASSWORD)["token"]
        response = api.patch_user(new_user.id, {"name": "some_new_name"}, token)
        assert response == {"status": "success"}

        user = api.get_user(new_user.id, token)
        assert user["name"] == "some_new_name"

    def test_patch_user_not_existed(self, root_user_token):

        with pytest.raises(api.HttpError) as error:
            api.patch_user(2, {"name": "some_new_name_2"}, root_user_token)

        assert error.value.status_code == 403
        assert error.value.message == {"status": "error", "description": "only owner has access"}

    def test_delete_user(self, new_user, root_user_token):
        token = api.login(new_user.name, DEFAULT_PASSWORD)["token"]
        response = api.delete_user(new_user.id, token)
        assert response == {"status": "success"}

        with pytest.raises(api.HttpError) as error:
            api.get_user(new_user.id, root_user_token)

        assert error.value.status_code == 404
        assert error.value.message == {"status": "error", "description": "User not found"}

    def test_delete_user_bad_token(self, new_user, root_user_token):

        with pytest.raises(api.HttpError) as error:
            api.delete_user(new_user.id, root_user_token)

        assert error.value.status_code == 403
        assert error.value.message == {"status": "error", "description": "only owner has access"}
