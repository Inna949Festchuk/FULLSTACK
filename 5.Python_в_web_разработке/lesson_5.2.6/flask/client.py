import requests

# response = requests.post(
#     "http://127.0.0.1:5000/hello/world/46",
#     json={"json_key_1": "json_val_1"},
#     params={'k1': 'v1'}, # query string заменяет такое "http://127.0.0.1:5000/hello/world/46?k1=v1"
#     headers={'token': 'xxx-xxxxx'} # Заголовок
# )

# print(response.status_code)
# print(response.json())

response = requests.post(
    "http://127.0.0.1:5000/user",
    json={"name": "user_26", "password": "admin"}
)

print(response.status_code)
print(response.json())