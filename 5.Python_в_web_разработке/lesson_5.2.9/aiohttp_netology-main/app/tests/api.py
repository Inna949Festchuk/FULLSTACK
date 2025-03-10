import requests
import json
from typing import Literal
from tests.config import API_URL


session = requests.Session()


class HttpError(Exception):
    def __init__(self, status_code: int, message: dict | str):
        self.status_code = status_code
        self.message = message


def base_request(method: Literal["get", "post", "delete", "patch"], path: str, *args, **kwargs) -> dict:
    print(f"{API_URL}/{path}")
    response: requests.Response = getattr(session, method)(f"{API_URL}/{path}", *args, **kwargs)
    if response.status_code >= 400:
        try:
            message = response.json()
        except json.decoder.JSONDecodeError:
            message = response.text

        raise HttpError(response.status_code, message)
    return response.json()


def login(name: str, password: str) -> dict:
    return base_request("post", "login", json={"name": name, "password": password})


def create_user(name: str, password: str) -> dict:
    return base_request("post", "users/", json={"name": name, "password": password})


def get_user(user_id: int, token: str) -> dict:
    return base_request("get", f"users/{user_id}", headers={"token": token})


def patch_user(user_id: int, patch: dict, token: str) -> dict:
    return base_request("patch", f"users/{user_id}", json=patch, headers={"token": token})


def delete_user(user_id: int, token: str) -> dict:
    return base_request("delete", f"users/{user_id}", headers={"token": token})
