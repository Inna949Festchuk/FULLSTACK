from __future__ import annotations

import requests


def main():
    url = "http://127.0.0.1:8080/v1/login/"
    payload = {"name": "admin", "password": "admin"}
    response = requests.post(url, json=payload).json()
    print(response)
    token = response["token"]

    response = requests.post(
        "http://127.0.0.1:8080/v1/right/",
        headers={
            "x-token": token,
        },
        json={
            "model": "Token",
            "read": True,
            "write": False,
            "only_own": False,
        },
    ).json()
    print(response)

    response = requests.patch(
        "http://127.0.0.1:8080/v1/right/5",
        json={"write": True},
        headers={"x-token": token},
    ).json()
    print(response)

    response = requests.get(
        "http://127.0.0.1:8080/v1/right",
        headers={"x-token": token},
    ).json()
    print(response)

    response = requests.get(
        "http://127.0.0.1:8080/v1/right?limit=2&page=3",
        headers={"x-token": token},
    ).json()
    print(response)

    response = requests.post(
        "http://127.0.0.1:8080/v1/user",
        json={"name": "test2", "password": "Ftest33rffAff"},
    ).json()
    print(response)


if __name__ == "__main__":
    main()
