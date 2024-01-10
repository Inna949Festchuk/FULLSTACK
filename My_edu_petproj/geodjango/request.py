# примеры API-запросов

##from pprint import pprint
##import requests
##
##url = 'http://127.0.0.1:8000/api/show_point/'
##
##def test_request():
##    
##    url = "http://127.0.0.1:8000/api/show_point/"
##    # params = {"model": "nike123"}
##    # headers = {"Autoriszation": "secret - token - 123"}
##    response = requests.get(url)
##    pprint(response)
##
##if __name__ == '__main__':
##    test_request()

# получение 
import requests
url = "http://127.0.0.1:8000/api/point/"
response = requests.get(url, headers={'Content-Type':'application/json'})
response.status_code
#200 - объект получен
response.json()
##Ответ
##[
##    {
##        'name': "'point2'", 'x': 954158.5, 'y': 4215137.5, 'location': 'SRID=4326;POINT (-95.33850006157502 29.72449988840415)'
##        },
##    {
##        'name': 'point3', 'x': 954159.0, 'y': 4215140.0, 'location': 'SRID=4326;POINT (-95.3384898245414 29.72452578636828)'
##        }
##    ]

##@baseUrl = 'http://127.0.0.1:8000/api/show_point/'
##GET {{baseUrl}}/show_point/
##Content-Type: application/json
###
# # В адресной строке браузера должен быть сформирован такой запрос:
# GET http://127.0.0.1:8000/api/show_point/

###
# создание point
# POST {{baseUrl}}/create_point/
# Content-Type: application/json

# {
#   "name": "point1",
#   "x": 954158.1,
#   "y": 4215137.1,
# }

###
# В адресной строке браузера должен быть сформирован такой запрос:
# POST http://127.0.0.1:8000/api/create_point/?name=point3&x=954159&y=4215140
import requests
url = "http://127.0.0.1:8000/api/point/"
response = requests.post(url, data={"name": "point1", "x": 954158.1, "y": 4215137.1, "location": "SRID=4326;POINT (954158.1 4215137.1)"})
response.status_code
#201 - объект создан

# обновление атрибута point
import requests
url = "http://127.0.0.1:8000/api/point/1/"
response = requests.patch(url, data={"name": "Измененное название точки"})
response.status_code
#200 - объект обновлен
