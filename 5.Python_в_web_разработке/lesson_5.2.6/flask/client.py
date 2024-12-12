import requests

# Создаем пользователя
# response = requests.post(
#     "http://127.0.0.1:5000/user",
#     json={"name": "user_38", "password": "12345678"}
# )

# Обновляем пользователя по id
response = requests.patch(
    "http://127.0.0.1:5000/user/1",
    json={"name": "new_user", "password": "admin12345"}
)
print(response.status_code)
print(response.json())

# Удаляем пользователя по id
# response = requests.delete(
#     "http://127.0.0.1:5000/user/18",
#     json={"name": "new_user", "password": "admin12345"}
# )
# print(response.status_code)
# print(response.json())

# Получаем пользователя по id
response = requests.get(
    "http://127.0.0.1:5000/user/1"
)

print(response.status_code)
print(response.json())

