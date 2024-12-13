import requests

# Создаем объявление
# response = requests.post(
#     "http://127.0.0.1:5000/press",
#     json={"title": "Первое объявление", "body": "Продам кота", "onwer": "Иванов А.А."}
# )

# print(response.status_code)
# print(response.json())

# Обновляем объявление по id
# response = requests.patch(
#     "http://127.0.0.1:5000/press/1",
#     json={"title": "Второе объявление", "body": "Продам рыжего кота", "onwer": "Иванов А.А."}
# )
# print(response.status_code)
# print(response.json())

# Удаляем объявление по id
# response = requests.delete(
#     "http://127.0.0.1:5000/press/1"
# )
# print(response.status_code)
# print(response.json())

# Получаем объявление по id
response = requests.get(
    "http://127.0.0.1:5000/press/1"
)

print(response.status_code)
print(response.json())

