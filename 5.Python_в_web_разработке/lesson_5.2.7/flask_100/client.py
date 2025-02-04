import requests

# response = requests.post(
#     "http://127.0.0.1:5000/user",
#     json={"name": "user_18", "password": "1234Ffeswder35"},
#
# )
# print(response.status_code)
# print(response.json())


response = requests.patch(
    "http://127.0.0.1:5000/user/18",
    json={"name": "new_user", "password": "1234FfFSFSfgge34eswder35"},
)
print(response.status_code)
print(response.json())

response = requests.delete(
    "http://127.0.0.1:5000/user/17",
)
print(response.status_code)
print(response.json())

response = requests.get(
    "http://127.0.0.1:5000/user/17",
)
print(response.status_code)
print(response.json())
