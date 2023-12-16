# примеры API-запросов

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
##        'name': "'point2'", 'x': '20 град 30 мин 50 с', 'y': '12 п.ш.', 'location': 'SRID=4326;POINT (954158.1 4215137.1)'
##        },
##    {
##        'name': 'point3', 'x': '35 град 10 мин 10 с', 'y': '55 п.ш.', 'location': 'SRID=4326;POINT (954158.1 4215137.1)'
##        }
##    ]

# создание point
import requests
url = "http://127.0.0.1:8000/api/point/"
response = requests.post(url, data={"name": "point1", "x": "-", "y": "-", "location": "SRID=4326;POINT (954158.1 4215137.1)"})
response.status_code
#201 - объект создан

# обновление атрибута point
import requests
url = "http://127.0.0.1:8000/api/point/1/"
response = requests.patch(url, data={"name": "Измененное название точки"})
response.status_code
#200 - объект обновлен
