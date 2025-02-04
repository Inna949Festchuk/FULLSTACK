import requests
import uuid
# response = requests.post(
#     " http://127.0.0.1:8080/v1/todo/",
#     json={"title": "t3", "description": "d", "important": True},
# )
# print(response.status_code)
# print(response.json())

# response = requests.patch(" http://127.0.0.1:8000/v1/todo/1/",
#                          json={"done": True, }
#                          )
# print(response.status_code)
# print(response.json())

# response = requests.delete(" http://127.0.0.1:8000/v1/todo/1/",
#                          )
# print(response.status_code)
# print(response.json())
#
# response = requests.get(" http://127.0.0.1:8000/v1/todo/1/",
#                          )
# print(response.status_code)
# print(response.json())


response = requests.post(" http://127.0.0.1:8000/v1/user/",
                         json={
                             "name": "user_2",
                             "password": "1234"
                         }
                         )
print(response.status_code)
print(response.json())

response = requests.post(" http://127.0.0.1:8000/v1/login/",
                         json={
                             "name": "user_2",
                             "password": "1234"
                         }
                         )
print(response.status_code)
token = response.json()["token"]
#

response = requests.post(
    " http://127.0.0.1:8000/v1/todo/",
    json={"title": "t4", "description": "d", "important": True},
    headers={"x-token": token}
)
print(response.status_code)
print(response.json())
todo_id = response.json()["id"]

#
# response = requests.post(" http://127.0.0.1:8000/v1/login/",
#                          json={
#                              "name": "user_1",
#                              "password": "1234"
#                          }
#                          )
# print(response.status_code)
# token = response.json()["token"]


response = requests.get(f"http://127.0.0.1:8000/v1/todo/{todo_id}/",
                            headers={"x-token": token}
                         )
print(response.status_code)
print(response.json())