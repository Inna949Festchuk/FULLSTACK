import requests

response = requests.post(
    " http://127.0.0.1:8080/v1/todo/",
    json={"title": "t3", "description": "d", "important": True},
)
print(response.status_code)
print(response.json())

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
