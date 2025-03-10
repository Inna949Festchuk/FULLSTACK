import pytest

from .api_client import HttpError, TodoApiClient
from .constants import DEFAULT_USER_PASSWORD


class TestRight:
    def test_get_rights(self, admin_client: TodoApiClient):
        response = admin_client.get_rights()
        assert response.page == 1
        assert response.total == 12
        assert len(response.rights) >= 0

    def test_get_rights_small_page(self, admin_client: TodoApiClient):
        response = admin_client.get_rights(page=1, limit=5)
        assert response.page == 1
        assert response.total == 12
        assert len(response.rights) == 5

        response_2 = admin_client.get_rights(page=2, limit=5)
        assert response_2.page == 2
        assert response_2.total == response.total
        assert len(response_2.rights) == 5
        assert response_2.rights != response.rights

        response_3 = admin_client.get_rights(page=3, limit=5)
        assert response_3.page == 3
        assert response_3.total == response.total
        assert len(response_3.rights) == 2
        assert response_3.rights != response.rights != response_2.rights

        assert len({*response.rights, *response_2.rights, *response_3.rights}) == 12

    def test_create_right(self, admin_client: TodoApiClient):
        response = None
        try:
            response = admin_client.create_right("token", True, False, False)
            assert response.id
            assert response.model == "token"
            assert response.write
            assert not response.read
            assert not response.only_own
        finally:
            if response:
                admin_client.delete_right(response.id)

    def test_delete_right(self, admin_client: TodoApiClient):
        response = admin_client.create_right("token", True, False, False)
        response_delete = admin_client.delete_right(response.id)
        assert response_delete.status == "deleted"
        with pytest.raises(HttpError) as err:
            admin_client.get_right(response.id)
        assert err.value.status_code == 404

    def test_non_priveleged_user(self, client: TodoApiClient, admin_client: TodoApiClient):
        client.create_user("test_non_priveleged_user", DEFAULT_USER_PASSWORD)
        client.auth("test_non_priveleged_user", DEFAULT_USER_PASSWORD)

        existed_rights = admin_client.get_rights()
        right = existed_rights.rights[0]

        with pytest.raises(HttpError) as err:
            client.delete_right(right.id)
        assert err.value.status_code == 403

        with pytest.raises(HttpError) as err:
            client.update_right(right.id, write=True, read=True, only_own=True)
        assert err.value.status_code == 403

        with pytest.raises(HttpError) as err:
            client.create_right("token", True, False, False)
        assert err.value.status_code == 403
