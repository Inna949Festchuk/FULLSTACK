import datetime

import pytest

from .api_client import HttpError, TodoApiClient
from .constants import DEFAULT_USER_PASSWORD


class TestUser:
    def test_create_user(self, client):
        request_time = datetime.datetime.utcnow()
        response = client.create_user("test_create_user", DEFAULT_USER_PASSWORD)
        response_time = datetime.datetime.utcnow()
        assert response.name == "test_create_user"
        assert request_time <= datetime.datetime.fromisoformat(response.registration_time) <= response_time

    def test_create_user_with_existing_name(self, client):
        client.create_user("test_create_user_with_existing_name", DEFAULT_USER_PASSWORD)
        with pytest.raises(HttpError) as err:
            client.create_user("test_create_user_with_existing_name", DEFAULT_USER_PASSWORD)
            assert err.value.status_code == 400

    def test_login(self, client):
        client.create_user("test_login", DEFAULT_USER_PASSWORD)
        response = client.login("test_login", DEFAULT_USER_PASSWORD)
        assert response.token is not None

    def test_get_user(self, client: TodoApiClient):
        create_response = client.create_user("test_get_user", DEFAULT_USER_PASSWORD)
        client.auth("test_get_user", DEFAULT_USER_PASSWORD)
        user = client.get_user(create_response.id)
        assert user.name == "test_get_user"

    def test_update_user_name(self, client: TodoApiClient):
        create_response = client.create_user("test_update_user_name", DEFAULT_USER_PASSWORD)
        client.auth("test_update_user_name", DEFAULT_USER_PASSWORD)
        update_response = client.update_user(create_response.id, name="test_update_user_name_new_name")
        assert update_response.name == "test_update_user_name_new_name"

    def test_update_user_password(self, client: TodoApiClient):
        create_response = client.create_user("test_update_user_password", DEFAULT_USER_PASSWORD)
        client.auth("test_update_user_password", DEFAULT_USER_PASSWORD)
        client.update_user(create_response.id, password="Ndd33eea3ND")
        login_response = client.login("test_update_user_password", "Ndd33eea3ND")
        assert login_response.token is not None

    def test_update_no_permission(self, client: TodoApiClient):
        client.create_user("test_update_no_permission", DEFAULT_USER_PASSWORD)
        client.auth("test_update_no_permission", DEFAULT_USER_PASSWORD)
        response = client.create_user("test_update_no_permission2", DEFAULT_USER_PASSWORD)
        with pytest.raises(HttpError) as err:
            client.update_user(response.id, name="test_update_no_permission_new_name")
        assert err.value.status_code == 403

    def test_delete_user(self, client: TodoApiClient, admin_client: TodoApiClient):
        create_response = client.create_user("test_delete_user", DEFAULT_USER_PASSWORD)
        user_id = create_response.id
        client.auth("test_delete_user", DEFAULT_USER_PASSWORD)
        delete_response = client.delete_user(create_response.id)
        assert delete_response.status == "deleted"
        with pytest.raises(HttpError) as err:
            client.get_user(user_id)
        assert err.value.status_code == 401  # token was deleted with user

        with pytest.raises(HttpError) as err:
            admin_client.get_user(user_id)
        assert err.value.status_code == 404
