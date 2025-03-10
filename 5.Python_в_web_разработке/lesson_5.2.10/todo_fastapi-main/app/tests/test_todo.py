import pytest

from .api_client import HttpError
from .conftest import NewUser, TodoApiClient
from .constants import NEW_TODO_ITEM_IMPORTANT, NEW_TODO_ITEM_NOT_IMPORTANT


class TestTodo:
    @pytest.mark.parametrize(
        "important",
        [
            True,
            False,
        ],
    )
    def test_create_todo(self, new_user: NewUser, important: bool):
        response = new_user.client.create_todo(name="test_create_todo", important=important)
        assert response.id is not None
        assert new_user.client.get_user(new_user.id).todos == [response.id]

    def test_create_todo_with_empty_name(self, new_user: NewUser):
        with pytest.raises(HttpError) as excinfo:
            new_user.client._call("POST", "/v1/todo", json={"important": False})
        assert excinfo.value.status_code == 422

    def test_create_todo_without_auth(self, client: TodoApiClient, client_without_auth: TodoApiClient):
        with pytest.raises(HttpError) as excinfo:
            client.create_todo("test_create_todo_without_auth")
        assert excinfo.value.status_code == 422

        with pytest.raises(HttpError) as excinfo:
            client_without_auth.create_todo("test_create_todo_without_auth")
        assert excinfo.value.status_code == 401

    def test_get_todos(self, new_user_with_todos: NewUser):
        todos = new_user_with_todos.client.get_todos().todos
        assert len(todos) == 2
        assert todos[0].name == NEW_TODO_ITEM_IMPORTANT
        assert todos[0].important is True
        assert todos[1].name == NEW_TODO_ITEM_NOT_IMPORTANT
        assert todos[1].important is False

    def test_get_todos_without_auth(self, client: TodoApiClient, client_without_auth: TodoApiClient):
        with pytest.raises(HttpError) as excinfo:
            client.get_todos()
        assert excinfo.value.status_code == 422

        with pytest.raises(HttpError) as excinfo:
            client_without_auth.get_todos()
        assert excinfo.value.status_code == 401

    def test_get_todo_id(self, new_user_with_todos: NewUser):
        todos = new_user_with_todos.client.get_todos().todos
        for todo in todos:
            todo_by_id = new_user_with_todos.client.get_todo(todo.id)
            assert todo_by_id.id == todo.id
            assert todo_by_id.name == todo.name
            assert todo_by_id.important == todo.important
            assert todo_by_id.done == todo.done
            assert todo_by_id.start_time == todo.start_time
            assert todo_by_id.finish_time == todo.finish_time

    #
    def test_get_todo_id_without_auth(self, client: TodoApiClient, client_without_auth: TodoApiClient):
        with pytest.raises(HttpError) as excinfo:
            client.get_todo(1)
        assert excinfo.value.status_code == 422

        with pytest.raises(HttpError) as excinfo:
            client_without_auth.get_todo(1)
        assert excinfo.value.status_code == 401

    def test_get_todo_id_with_wrong_id(self, new_user_with_todos: NewUser):
        with pytest.raises(HttpError) as excinfo:
            new_user_with_todos.client.get_todo(9999999)
        assert excinfo.value.status_code == 404

    def test_get_todo_id_not_owner(self, user_client: TodoApiClient, new_user_with_todos: NewUser):
        todos = new_user_with_todos.client.get_todos().todos
        for todo in todos:
            with pytest.raises(HttpError) as excinfo:
                user_client.get_todo(todo.id)
            assert excinfo.value.status_code == 403

    def test_update_todo_name(self, new_user_with_todos: NewUser):
        todo = new_user_with_todos.client.get_todos().todos[0]
        new_user_with_todos.client.update_todo(todo.id, name="new_name")
        todo = new_user_with_todos.client.get_todo(todo.id)
        assert todo.name == "new_name"

    def test_update_todo_important(self, new_user_with_todos: NewUser):
        todo = new_user_with_todos.client.get_todos().todos[0]
        new_user_with_todos.client.update_todo(todo.id, important=True)
        todo = new_user_with_todos.client.get_todo(todo.id)
        assert todo.important is True

    def test_update_todo_done(self, new_user_with_todos: NewUser):
        todo = new_user_with_todos.client.get_todos().todos[0]
        new_user_with_todos.client.update_todo(todo.id, done=True)
        todo = new_user_with_todos.client.get_todo(todo.id)
        assert todo.done is True
        assert todo.finish_time is not None

    def test_delete_todo(self, new_user_with_todos: NewUser):
        todo = new_user_with_todos.client.get_todos().todos[0]
        new_user_with_todos.client.delete_todo(todo.id)
        with pytest.raises(HttpError) as excinfo:
            new_user_with_todos.client.get_todo(todo.id)
        assert excinfo.value.status_code == 404

    def test_update_alien_todo(self, new_user_with_todos: NewUser, user_client: TodoApiClient):
        todo = new_user_with_todos.client.get_todos().todos[0]
        with pytest.raises(HttpError) as excinfo:
            user_client.update_todo(todo.id, name="new_name")
        assert excinfo.value.status_code == 403

    def test_admin_update_alien_todo(self, new_user_with_todos: NewUser, admin_client: TodoApiClient):
        todo = new_user_with_todos.client.get_todos().todos[0]
        admin_client.update_todo(todo.id, name="new_name")
        todo = new_user_with_todos.client.get_todo(todo.id)
        assert todo.name == "new_name"
