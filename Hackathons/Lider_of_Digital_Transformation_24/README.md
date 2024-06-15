# Хакатон ЛЦТ 2024
# Мобильное приложение для управления антропогенной нагрузкой на особо охраняемых природных территориях Камчатского края

## **Настройка сервиса**
### Создаем виртуальную среду
```cmd
python -m venv venv
```
### Активируем среду
```cmd
venv\Scripts\activate
```
### Скачиваем библиотеки
```cmd
python -m pip install -r requirements.txt
```
### Устанавливаем СУБД Postgresql
### Устанавливаем дополнение для работы с геопространственными данными PostGIS 
### На основе шаблонной БД PostGIS создаем свою базу данных
```
### Запускаем утилиту psql 
```cmd
psql
```
### Создаем пользователя
```cmd
CREATE USER admin WITH PASSWORD 'admin';
``` 
### Создаем БД test с собственником admin
```cmd
CREATE DATABASE test OWNER admin ENCODING 'UTF8';
\q
```
### Создаем миграции
```cmd
python manage.py makemigrations
```
### Мигрируем (пересоздать БД если не мигрируется)
```cmd
python manage.py migrate
```
### Загружаем данные из фикстуры geodjango/geoapp/data/DataSource.json в БД
```cmd
python manage.py import_json -c
```
### Создаум суперюзера для доступа к административной панели django
```cmd
python manage.py createsuperuser
Username: admin
Password: admin
```
### Устанавливаем расширения PostGIS, переходим в  нашу БД test
```cmd
psql test
```
### Устанавливаем расширение postgresql для созданной БД
```cmd
CREATE EXTENSION <название расширения>;
\q
```

### Переходим в корневую дирректорию проекта и запускаем его (остановка сервера Ctrl+C)
```cmd
python manage.py runserver
```
## **Работа с сервисом**
### *Для тестовой демонстрации к сервису организован удаленный доступ с применение туннелирования (сервис Ngrok) поэтому вы уже можите начать им пользоваться*

### Загрузка маршрутов по данным GPS наблюдений в базу данных (сисадмин)
- подготовить файл конвертировав его из формата .gpx в .geojson (использовать инструментарий ГИС, в данный момент не реализовано)
- после того как инфраструктура проекта geodjango развернута в коде geodjango/geoapp/management/commands/import_json.py задать путь и в терминале выполнить команду, маршрут загрузится в БД и отобразится на карте, также по этой команде будет произведен расчет для движения по местности с помощью компаса по азимутам магнитным
```bash
python manage.py import_json -c
```
### Работа с сервисом в роли "Турист"
- переходим по https://swan-decent-shrew.ngrok-free.app/api/map/
- видим карту на ней маршрут, карту можно маштабировать, приблизив можно увидеть точки маршрута, нажав на линию во всплывающем окне можно увидеть информацию (азимут, расстояние)
- слои можно подключать отключать
- карту можно перевести в режим "ОФФЛАЙН" нажав соответствующую кнопку (при этом вся необходимая информация выгрузится в кеш браузера и появится информационное сообщение)
- предусмотрены кнопки старта маршрута и отметки его завершения, по нажатию этих кнопок высчитывается время пребывания туристов на маршруте (при появленнии сети эти данные отправляются в базу данных, **так можно расчитывать антропогенную нагрузку в районе пешеходных троп с учетом количества туристов в группе и времени нахождения их на маршруте**
- Двигаясь по маршруту турист может пользоваться компасом, сверяясь с данными азимутов магнитных указанных на карте, все замеченные инциденты отмечаются путем нанесения маркеров на карте
- Так как карта нахлдится в режиме оффлайн данные метки также записываются в кеш и с появлением сети могут быть отправлены администратору путем нажатия кнопки "Отправить данные"
### Работа с административной панелью 
- переходим по https://swan-decent-shrew.ngrok-free.app/admin/
- вводим имя: admin, пароль: admin
- видим таблицу инцидентов (жалоб туристов)
- видим таблицу точек GPS
- видим таблицу маршрута с расчитанными значениями ориентиров, азимутов магнитных, расстояний в парах шагов от ориентира к ориентиру
- видим таблицу егерей
- видим таблицу назначений, с помощью этой таблицы администратор распределяет поступившие от туристов задачи (жалобы) между егерями
### Работа с сервисом в роли "Егерь"
- переходим по https://swan-decent-shrew.ngrok-free.app/api/webtask/
- видим карту с поступившими задачами 
- листаем вниз видим список егерей, назначенные им задачи, координаты этих задач, кнопку отобразить на карте
- нажимаем кнопку отобразить на карте, проиложение подымает страницу к карте и центрирует метку с задачей, подписывая ее
- если задача выполнена (проконтролирована) администратор удаляет этот инциндент (жалобу) из базы данных и задача автоматически удаляется из этого приложения егеря

### Решение
### [Архив с программой обработки спутниковых снимков, пояснительная записка и датасеты (Landsat-8)](https://disk.yandex.ru/d/dkFScD3WmXYQIw)
>>>>>>> fff6526c8cb0472cc40b32cfbd68f10d281cf22b

#### АПИ создания метки инцидента:
```python
import requests
url = " https://swan-decent-shrew.ngrok-free.app/api/create_point/"
response = requests.post(url, data={"name": "test", "location": "SRID=4326;POINT (158.8025665283203 53.5190837863296)"})
response.json()
```
#### Запрос на JS
```js
// Пишем функцию получения CSRF-токен (он нужен для POST-запрооса) из куки 
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        // Проверяем, начинается ли куки с искомого имени
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
        // Извлекаем значение куки
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
        }
    }
    }
    return cookieValue;
}

// Добавляем маркер
function saveMarkerToDatabase(coordinates, markerName) {
            fetch('https://swan-decent-shrew.ngrok-free.app/api/create_point/', {
                // Задаем метод REST-запроса
                method: 'POST',
                // Формируем хедер запроса
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'), // Добавляем CSRF-токен в заголовок запроса
                },
                // Формируем тело запроса
                body: JSON.stringify({ name: markerName, location: 'SRID=4326;POINT(' + coordinates.lng + ' ' + coordinates.lat + ')' })
         })
            // Получаем ответ на запрос
            .then(response => response.json())
            .then(data => {
              console.log(data);
            })
            
            .catch((error) => {
                console.error('Ошибка сохранения маркера:', error);
            });
}
```

#### Ответ:
```py
запрос успешно отработал
'Данные переданы службам реагирования! С Вами свяжется оператор.'
# или если в базе уже есть эти данные 
'Эти данные уже были переданы ранее'
```

#### АПИ создания выдачи маршрута (активация оффлайн)
```py
import requests
url = "https://swan-decent-shrew.ngrok-free.app/api/trek/"
response = requests.post(url)
response.json()
```
#### Запрос на JS
```js
document.getElementById('getDataButton').addEventListener('click', function() {
          fetch('https://swan-decent-shrew.ngrok-free.app/api/trek/', {
            method: 'GET',
            headers: {
              'Content-Type': 'application/json'
            }
          })
          .then(response => response.json())
          .then(data => {
            // Словарь geoJSON выгруженный из базы данных
            var trek_points = data.context_point_trek.features;
            var trek_lines = data.context_lines_trek.features;

            // Сохранение trek_points в локальное хранилище
            localStorage.setItem('savedTrekPoints', JSON.stringify(trek_points));

            // Сохранение trek_lines в локальное хранилище
            localStorage.setItem('savedTrekLines', JSON.stringify(trek_lines));
            
            alert('Ваш маршрут загружен! Режим "ОФФЛАЙН" активен!');

            console.log('Ваш маршрут загружен! Режим "ОФФЛАЙН" активен!')
          })
          .catch(error => {
            console.error('Ошибка:', error);
          });
        });
```
#### Ответ:

<details>
{
    "context_point_trek": {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:4326"
            }
        },
        "features": [
            {
                "type": "Feature",
                "id": 1,
                "properties": {
                    "name": "Точка: 1"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.839538,
                        53.572238
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 2,
                "properties": {
                    "name": "Точка: 2"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83972,
                        53.572024
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 3,
                "properties": {
                    "name": "Точка: 3"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83974,
                        53.571802
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 4,
                "properties": {
                    "name": "Точка: 4"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83948,
                        53.571605
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 5,
                "properties": {
                    "name": "Точка: 5"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83958,
                        53.571379
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 6,
                "properties": {
                    "name": "Точка: 6"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83979,
                        53.571132
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 7,
                "properties": {
                    "name": "Точка: 7"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83982,
                        53.571048
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 8,
                "properties": {
                    "name": "Точка: 8"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8403,
                        53.570702
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 9,
                "properties": {
                    "name": "Точка: 9"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84041,
                        53.570419
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 10,
                "properties": {
                    "name": "Точка: 10"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84033,
                        53.570316
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 11,
                "properties": {
                    "name": "Точка: 11"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84075,
                        53.57005
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 12,
                "properties": {
                    "name": "Точка: 12"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84124,
                        53.569633
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 13,
                "properties": {
                    "name": "Точка: 13"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84126,
                        53.569483
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 14,
                "properties": {
                    "name": "Точка: 14"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84122,
                        53.569401
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 15,
                "properties": {
                    "name": "Точка: 15"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84122,
                        53.569206
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 16,
                "properties": {
                    "name": "Точка: 16"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84126,
                        53.568774
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 17,
                "properties": {
                    "name": "Точка: 17"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84119,
                        53.568748
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 18,
                "properties": {
                    "name": "Точка: 18"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84117,
                        53.568494
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 19,
                "properties": {
                    "name": "Точка: 19"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84121,
                        53.568045
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 20,
                "properties": {
                    "name": "Точка: 20"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84117,
                        53.567925
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 21,
                "properties": {
                    "name": "Точка: 21"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84125,
                        53.567677
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 22,
                "properties": {
                    "name": "Точка: 22"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84122,
                        53.567363
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 23,
                "properties": {
                    "name": "Точка: 23"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84132,
                        53.567213
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 24,
                "properties": {
                    "name": "Точка: 24"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84137,
                        53.567038
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 25,
                "properties": {
                    "name": "Точка: 25"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8414,
                        53.566788
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 26,
                "properties": {
                    "name": "Точка: 26"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84133,
                        53.566478
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 27,
                "properties": {
                    "name": "Точка: 27"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84147,
                        53.566182
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 28,
                "properties": {
                    "name": "Точка: 28"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84146,
                        53.565999
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 29,
                "properties": {
                    "name": "Точка: 29"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84161,
                        53.565372
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 30,
                "properties": {
                    "name": "Точка: 30"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84159,
                        53.565206
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 31,
                "properties": {
                    "name": "Точка: 31"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84176,
                        53.564743
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 32,
                "properties": {
                    "name": "Точка: 32"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84169,
                        53.564591
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 33,
                "properties": {
                    "name": "Точка: 33"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84158,
                        53.564521
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 34,
                "properties": {
                    "name": "Точка: 34"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84152,
                        53.564062
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 35,
                "properties": {
                    "name": "Точка: 35"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84139,
                        53.563784
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 36,
                "properties": {
                    "name": "Точка: 36"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84045,
                        53.563151
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 37,
                "properties": {
                    "name": "Точка: 37"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.84032,
                        53.562979
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 38,
                "properties": {
                    "name": "Точка: 38"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8401,
                        53.562862
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 39,
                "properties": {
                    "name": "Точка: 39"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83994,
                        53.562874
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 40,
                "properties": {
                    "name": "Точка: 40"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83969,
                        53.562624
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 41,
                "properties": {
                    "name": "Точка: 41"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83952,
                        53.562381
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 42,
                "properties": {
                    "name": "Точка: 42"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83926,
                        53.562138
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 43,
                "properties": {
                    "name": "Точка: 43"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83896,
                        53.562045
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 44,
                "properties": {
                    "name": "Точка: 44"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83874,
                        53.56193
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 45,
                "properties": {
                    "name": "Точка: 45"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83859,
                        53.561754
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 46,
                "properties": {
                    "name": "Точка: 46"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83846,
                        53.561709
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 47,
                "properties": {
                    "name": "Точка: 47"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83833,
                        53.56158
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 48,
                "properties": {
                    "name": "Точка: 48"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83812,
                        53.561279
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 49,
                "properties": {
                    "name": "Точка: 49"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83797,
                        53.561179
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 50,
                "properties": {
                    "name": "Точка: 50"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83791,
                        53.561018
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 51,
                "properties": {
                    "name": "Точка: 51"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83769,
                        53.560811
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 52,
                "properties": {
                    "name": "Точка: 52"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83766,
                        53.560741
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 53,
                "properties": {
                    "name": "Точка: 53"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83751,
                        53.560654
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 54,
                "properties": {
                    "name": "Точка: 54"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83742,
                        53.560558
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 55,
                "properties": {
                    "name": "Точка: 55"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83722,
                        53.560467
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 56,
                "properties": {
                    "name": "Точка: 56"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83674,
                        53.559997
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 57,
                "properties": {
                    "name": "Точка: 57"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83645,
                        53.559851
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 58,
                "properties": {
                    "name": "Точка: 58"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83608,
                        53.559729
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 59,
                "properties": {
                    "name": "Точка: 59"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83591,
                        53.559616
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 60,
                "properties": {
                    "name": "Точка: 60"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83562,
                        53.559598
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 61,
                "properties": {
                    "name": "Точка: 61"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83512,
                        53.559363
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 62,
                "properties": {
                    "name": "Точка: 62"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83491,
                        53.559221
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 63,
                "properties": {
                    "name": "Точка: 63"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83475,
                        53.559168
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 64,
                "properties": {
                    "name": "Точка: 64"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83455,
                        53.558778
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 65,
                "properties": {
                    "name": "Точка: 65"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83443,
                        53.558663
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 66,
                "properties": {
                    "name": "Точка: 66"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83423,
                        53.558543
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 67,
                "properties": {
                    "name": "Точка: 67"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83397,
                        53.55827
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 68,
                "properties": {
                    "name": "Точка: 68"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83392,
                        53.558118
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 69,
                "properties": {
                    "name": "Точка: 69"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8339,
                        53.557865
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 70,
                "properties": {
                    "name": "Точка: 70"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83378,
                        53.557575
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 71,
                "properties": {
                    "name": "Точка: 71"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83349,
                        53.557358
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 72,
                "properties": {
                    "name": "Точка: 72"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83324,
                        53.557021
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 73,
                "properties": {
                    "name": "Точка: 73"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83307,
                        53.556893
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 74,
                "properties": {
                    "name": "Точка: 74"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83274,
                        53.556734
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 75,
                "properties": {
                    "name": "Точка: 75"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83217,
                        53.556516
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 76,
                "properties": {
                    "name": "Точка: 76"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83183,
                        53.556229
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 77,
                "properties": {
                    "name": "Точка: 77"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83102,
                        53.555896
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 78,
                "properties": {
                    "name": "Точка: 78"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83091,
                        53.555905
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 79,
                "properties": {
                    "name": "Точка: 79"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.83012,
                        53.555738
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 80,
                "properties": {
                    "name": "Точка: 80"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8298,
                        53.555746
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 81,
                "properties": {
                    "name": "Точка: 81"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82946,
                        53.555709
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 82,
                "properties": {
                    "name": "Точка: 82"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82906,
                        53.555518
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 83,
                "properties": {
                    "name": "Точка: 83"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8288500000001,
                        53.555458
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 84,
                "properties": {
                    "name": "Точка: 84"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82855,
                        53.555521
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 85,
                "properties": {
                    "name": "Точка: 85"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82827,
                        53.555473
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 86,
                "properties": {
                    "name": "Точка: 86"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82808,
                        53.555482
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 87,
                "properties": {
                    "name": "Точка: 87"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82744,
                        53.555342
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 88,
                "properties": {
                    "name": "Точка: 88"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82727,
                        53.55526
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 89,
                "properties": {
                    "name": "Точка: 89"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82706,
                        53.555217
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 90,
                "properties": {
                    "name": "Точка: 90"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82687,
                        53.555229
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 91,
                "properties": {
                    "name": "Точка: 91"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82661,
                        53.555185
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 92,
                "properties": {
                    "name": "Точка: 92"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82581,
                        53.555154
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 93,
                "properties": {
                    "name": "Точка: 93"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82524,
                        53.555075
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 94,
                "properties": {
                    "name": "Точка: 94"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82507,
                        53.555006
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 95,
                "properties": {
                    "name": "Точка: 95"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82453,
                        53.554986
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 96,
                "properties": {
                    "name": "Точка: 96"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82353,
                        53.554819
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 97,
                "properties": {
                    "name": "Точка: 97"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82301,
                        53.554481
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 98,
                "properties": {
                    "name": "Точка: 98"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8229,
                        53.554451
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 99,
                "properties": {
                    "name": "Точка: 99"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82275,
                        53.55425
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 100,
                "properties": {
                    "name": "Точка: 100"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82241,
                        53.553967
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 101,
                "properties": {
                    "name": "Точка: 101"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8223,
                        53.553815
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 102,
                "properties": {
                    "name": "Точка: 102"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82207,
                        53.553677
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 103,
                "properties": {
                    "name": "Точка: 103"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82197,
                        53.553658
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 104,
                "properties": {
                    "name": "Точка: 104"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82183,
                        53.553554
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 105,
                "properties": {
                    "name": "Точка: 105"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82179,
                        53.553452
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 106,
                "properties": {
                    "name": "Точка: 106"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82152,
                        53.553407
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 107,
                "properties": {
                    "name": "Точка: 107"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82162,
                        53.553401
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 108,
                "properties": {
                    "name": "Точка: 108"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82158,
                        53.553358
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 109,
                "properties": {
                    "name": "Точка: 109"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82157,
                        53.553269
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 110,
                "properties": {
                    "name": "Точка: 110"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8214,
                        53.553067
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 111,
                "properties": {
                    "name": "Точка: 111"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8210600000001,
                        53.552871
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 112,
                "properties": {
                    "name": "Точка: 112"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82073,
                        53.55273
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 113,
                "properties": {
                    "name": "Точка: 113"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.82,
                        53.552492
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 114,
                "properties": {
                    "name": "Точка: 114"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81976,
                        53.552474
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 115,
                "properties": {
                    "name": "Точка: 115"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8191,
                        53.552327
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 116,
                "properties": {
                    "name": "Точка: 116"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81846,
                        53.552158
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 117,
                "properties": {
                    "name": "Точка: 117"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81807,
                        53.551981
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 118,
                "properties": {
                    "name": "Точка: 118"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81697,
                        53.551723
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 119,
                "properties": {
                    "name": "Точка: 119"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81595,
                        53.551318
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 120,
                "properties": {
                    "name": "Точка: 120"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81552,
                        53.551196
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 121,
                "properties": {
                    "name": "Точка: 121"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81456,
                        53.551014
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 122,
                "properties": {
                    "name": "Точка: 122"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81425,
                        53.550872
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 123,
                "properties": {
                    "name": "Точка: 123"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81397,
                        53.550825
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 124,
                "properties": {
                    "name": "Точка: 124"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81377,
                        53.550693
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 125,
                "properties": {
                    "name": "Точка: 125"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81328,
                        53.550578
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 126,
                "properties": {
                    "name": "Точка: 126"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81277,
                        53.550345
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 127,
                "properties": {
                    "name": "Точка: 127"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81212,
                        53.550122
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 128,
                "properties": {
                    "name": "Точка: 128"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81153,
                        53.550022
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 129,
                "properties": {
                    "name": "Точка: 129"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81026,
                        53.549594
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 130,
                "properties": {
                    "name": "Точка: 130"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81023,
                        53.549253
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 131,
                "properties": {
                    "name": "Точка: 131"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81029,
                        53.549206
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 132,
                "properties": {
                    "name": "Точка: 132"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81016,
                        53.549114
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 133,
                "properties": {
                    "name": "Точка: 133"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81006,
                        53.54897
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 134,
                "properties": {
                    "name": "Точка: 134"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81006,
                        53.548887
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 135,
                "properties": {
                    "name": "Точка: 135"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80943,
                        53.548639
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 136,
                "properties": {
                    "name": "Точка: 136"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80931,
                        53.548552
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 137,
                "properties": {
                    "name": "Точка: 137"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80924,
                        53.548392
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 138,
                "properties": {
                    "name": "Точка: 138"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80942,
                        53.548162
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 139,
                "properties": {
                    "name": "Точка: 139"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80952,
                        53.548115
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 140,
                "properties": {
                    "name": "Точка: 140"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80975,
                        53.547898
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 141,
                "properties": {
                    "name": "Точка: 141"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80976,
                        53.547726
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 142,
                "properties": {
                    "name": "Точка: 142"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80983,
                        53.547507
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 143,
                "properties": {
                    "name": "Точка: 143"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80998,
                        53.547365
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 144,
                "properties": {
                    "name": "Точка: 144"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81013,
                        53.547143
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 145,
                "properties": {
                    "name": "Точка: 145"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81012,
                        53.547082
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 146,
                "properties": {
                    "name": "Точка: 146"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81032,
                        53.54664
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 147,
                "properties": {
                    "name": "Точка: 147"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81067,
                        53.546048
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 148,
                "properties": {
                    "name": "Точка: 148"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81078,
                        53.545795
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 149,
                "properties": {
                    "name": "Точка: 149"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81108,
                        53.545518
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 150,
                "properties": {
                    "name": "Точка: 150"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81116,
                        53.544957
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 151,
                "properties": {
                    "name": "Точка: 151"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81109,
                        53.54467
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 152,
                "properties": {
                    "name": "Точка: 152"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81114,
                        53.544376
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 153,
                "properties": {
                    "name": "Точка: 153"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81082,
                        53.543883
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 154,
                "properties": {
                    "name": "Точка: 154"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81079,
                        53.543549
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 155,
                "properties": {
                    "name": "Точка: 155"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81054,
                        53.543046
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 156,
                "properties": {
                    "name": "Точка: 156"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81061,
                        53.542848
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 157,
                "properties": {
                    "name": "Точка: 157"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81059,
                        53.542669
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 158,
                "properties": {
                    "name": "Точка: 158"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81041,
                        53.542373
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 159,
                "properties": {
                    "name": "Точка: 159"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.81028,
                        53.542252
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 160,
                "properties": {
                    "name": "Точка: 160"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80999,
                        53.541674
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 161,
                "properties": {
                    "name": "Точка: 161"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80999,
                        53.541594
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 162,
                "properties": {
                    "name": "Точка: 162"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80993,
                        53.541519
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 163,
                "properties": {
                    "name": "Точка: 163"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80989,
                        53.541363
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 164,
                "properties": {
                    "name": "Точка: 164"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80977,
                        53.541264
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 165,
                "properties": {
                    "name": "Точка: 165"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8097,
                        53.540808
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 166,
                "properties": {
                    "name": "Точка: 166"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80957,
                        53.540526
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 167,
                "properties": {
                    "name": "Точка: 167"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80956,
                        53.540391
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 168,
                "properties": {
                    "name": "Точка: 168"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80949,
                        53.540216
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 169,
                "properties": {
                    "name": "Точка: 169"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80941,
                        53.540104
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 170,
                "properties": {
                    "name": "Точка: 170"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80909,
                        53.539997
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 171,
                "properties": {
                    "name": "Точка: 171"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80862,
                        53.539939
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 172,
                "properties": {
                    "name": "Точка: 172"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80828,
                        53.539719
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 173,
                "properties": {
                    "name": "Точка: 173"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80783,
                        53.5395
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 174,
                "properties": {
                    "name": "Точка: 174"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80739,
                        53.539491
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 175,
                "properties": {
                    "name": "Точка: 175"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80708,
                        53.539525
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 176,
                "properties": {
                    "name": "Точка: 176"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80687,
                        53.539473
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 177,
                "properties": {
                    "name": "Точка: 177"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80672,
                        53.539388
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 178,
                "properties": {
                    "name": "Точка: 178"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80647,
                        53.539382
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 179,
                "properties": {
                    "name": "Точка: 179"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80589,
                        53.539233
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 180,
                "properties": {
                    "name": "Точка: 180"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80507,
                        53.539096
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 181,
                "properties": {
                    "name": "Точка: 181"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8047600000001,
                        53.53896
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 182,
                "properties": {
                    "name": "Точка: 182"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80455,
                        53.538926
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 183,
                "properties": {
                    "name": "Точка: 183"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8036,
                        53.538924
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 184,
                "properties": {
                    "name": "Точка: 184"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80281,
                        53.539079
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 185,
                "properties": {
                    "name": "Точка: 185"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80253,
                        53.539201
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 186,
                "properties": {
                    "name": "Точка: 186"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80229,
                        53.539254
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 187,
                "properties": {
                    "name": "Точка: 187"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80209,
                        53.539267
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 188,
                "properties": {
                    "name": "Точка: 188"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.8017,
                        53.539169
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 189,
                "properties": {
                    "name": "Точка: 189"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80093,
                        53.53919
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 190,
                "properties": {
                    "name": "Точка: 190"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.80055,
                        53.53927
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 191,
                "properties": {
                    "name": "Точка: 191"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79971,
                        53.539345
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 192,
                "properties": {
                    "name": "Точка: 192"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79892,
                        53.539286
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 193,
                "properties": {
                    "name": "Точка: 193"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79863,
                        53.539324
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 194,
                "properties": {
                    "name": "Точка: 194"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79792,
                        53.539209
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 195,
                "properties": {
                    "name": "Точка: 195"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79762,
                        53.539111
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 196,
                "properties": {
                    "name": "Точка: 196"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79714,
                        53.539058
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 197,
                "properties": {
                    "name": "Точка: 197"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79577,
                        53.538539
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 198,
                "properties": {
                    "name": "Точка: 198"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79537,
                        53.538363
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 199,
                "properties": {
                    "name": "Точка: 199"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79522,
                        53.53824
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 200,
                "properties": {
                    "name": "Точка: 200"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79481,
                        53.53811
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 201,
                "properties": {
                    "name": "Точка: 201"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79465,
                        53.538093
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 202,
                "properties": {
                    "name": "Точка: 202"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7945,
                        53.538026
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 203,
                "properties": {
                    "name": "Точка: 203"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79432,
                        53.537894
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 204,
                "properties": {
                    "name": "Точка: 204"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79405,
                        53.537565
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 205,
                "properties": {
                    "name": "Точка: 205"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79364,
                        53.537306
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 206,
                "properties": {
                    "name": "Точка: 206"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79288,
                        53.536953
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 207,
                "properties": {
                    "name": "Точка: 207"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79277,
                        53.536744
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 208,
                "properties": {
                    "name": "Точка: 208"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79256,
                        53.536705
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 209,
                "properties": {
                    "name": "Точка: 209"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79208,
                        53.53648
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 210,
                "properties": {
                    "name": "Точка: 210"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79151,
                        53.535838
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 211,
                "properties": {
                    "name": "Точка: 211"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79123,
                        53.535594
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 212,
                "properties": {
                    "name": "Точка: 212"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79085,
                        53.535428
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 213,
                "properties": {
                    "name": "Точка: 213"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79032,
                        53.535015
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 214,
                "properties": {
                    "name": "Точка: 214"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79016,
                        53.534986
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 215,
                "properties": {
                    "name": "Точка: 215"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.79004,
                        53.534852
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 216,
                "properties": {
                    "name": "Точка: 216"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78974,
                        53.534627
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 217,
                "properties": {
                    "name": "Точка: 217"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78951,
                        53.534499
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 218,
                "properties": {
                    "name": "Точка: 218"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7892,
                        53.534245
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 219,
                "properties": {
                    "name": "Точка: 219"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78912,
                        53.534231
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 220,
                "properties": {
                    "name": "Точка: 220"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78888,
                        53.533986
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 221,
                "properties": {
                    "name": "Точка: 221"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7888,
                        53.533851
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 222,
                "properties": {
                    "name": "Точка: 222"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78844,
                        53.53368
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 223,
                "properties": {
                    "name": "Точка: 223"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78842,
                        53.533619
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 224,
                "properties": {
                    "name": "Точка: 224"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78829,
                        53.533546
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 225,
                "properties": {
                    "name": "Точка: 225"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78816,
                        53.533407
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 226,
                "properties": {
                    "name": "Точка: 226"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78813,
                        53.533299
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 227,
                "properties": {
                    "name": "Точка: 227"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78786,
                        53.533015
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 228,
                "properties": {
                    "name": "Точка: 228"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78727,
                        53.532711
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 229,
                "properties": {
                    "name": "Точка: 229"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78696,
                        53.532303
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 230,
                "properties": {
                    "name": "Точка: 230"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78688,
                        53.532245
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 231,
                "properties": {
                    "name": "Точка: 231"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78671,
                        53.532211
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 232,
                "properties": {
                    "name": "Точка: 232"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78641,
                        53.531988
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 233,
                "properties": {
                    "name": "Точка: 233"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78611,
                        53.53161
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 234,
                "properties": {
                    "name": "Точка: 234"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7861,
                        53.531546
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 235,
                "properties": {
                    "name": "Точка: 235"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78596,
                        53.531335
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 236,
                "properties": {
                    "name": "Точка: 236"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7859,
                        53.531068
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 237,
                "properties": {
                    "name": "Точка: 237"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78581,
                        53.530967
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 238,
                "properties": {
                    "name": "Точка: 238"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7852,
                        53.530821
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 239,
                "properties": {
                    "name": "Точка: 239"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78494,
                        53.530635
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 240,
                "properties": {
                    "name": "Точка: 240"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78458,
                        53.530562
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 241,
                "properties": {
                    "name": "Точка: 241"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78431,
                        53.530428
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 242,
                "properties": {
                    "name": "Точка: 242"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78421,
                        53.530243
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 243,
                "properties": {
                    "name": "Точка: 243"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78404,
                        53.53009
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 244,
                "properties": {
                    "name": "Точка: 244"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78331,
                        53.529769
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 245,
                "properties": {
                    "name": "Точка: 245"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78321,
                        53.529467
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 246,
                "properties": {
                    "name": "Точка: 246"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78294,
                        53.529095
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 247,
                "properties": {
                    "name": "Точка: 247"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78286,
                        53.528902
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 248,
                "properties": {
                    "name": "Точка: 248"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78269,
                        53.528769
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 249,
                "properties": {
                    "name": "Точка: 249"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78234,
                        53.528322
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 250,
                "properties": {
                    "name": "Точка: 250"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78225,
                        53.52816
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 251,
                "properties": {
                    "name": "Точка: 251"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78237,
                        53.527858
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 252,
                "properties": {
                    "name": "Точка: 252"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78223,
                        53.527545
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 253,
                "properties": {
                    "name": "Точка: 253"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78219,
                        53.52729
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 254,
                "properties": {
                    "name": "Точка: 254"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78207,
                        53.527189
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 255,
                "properties": {
                    "name": "Точка: 255"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7817500000001,
                        53.526708
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 256,
                "properties": {
                    "name": "Точка: 256"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7815700000001,
                        53.52666
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 257,
                "properties": {
                    "name": "Точка: 257"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78133,
                        53.526404
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 258,
                "properties": {
                    "name": "Точка: 258"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7812100000001,
                        53.526423
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 259,
                "properties": {
                    "name": "Точка: 259"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78114,
                        53.526392
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 260,
                "properties": {
                    "name": "Точка: 260"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78102,
                        53.526231
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 261,
                "properties": {
                    "name": "Точка: 261"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7807,
                        53.526121
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 262,
                "properties": {
                    "name": "Точка: 262"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78051,
                        53.525995
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 263,
                "properties": {
                    "name": "Точка: 263"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7801,
                        53.525899
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 264,
                "properties": {
                    "name": "Точка: 264"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.78004,
                        53.525737
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 265,
                "properties": {
                    "name": "Точка: 265"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77992,
                        53.525587
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 266,
                "properties": {
                    "name": "Точка: 266"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77918,
                        53.525514
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 267,
                "properties": {
                    "name": "Точка: 267"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77914,
                        53.525361
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 268,
                "properties": {
                    "name": "Точка: 268"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77887,
                        53.525253
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 269,
                "properties": {
                    "name": "Точка: 269"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77869,
                        53.525146
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 270,
                "properties": {
                    "name": "Точка: 270"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77869,
                        53.525097
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 271,
                "properties": {
                    "name": "Точка: 271"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77861,
                        53.525048
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 272,
                "properties": {
                    "name": "Точка: 272"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77824,
                        53.524942
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 273,
                "properties": {
                    "name": "Точка: 273"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77788,
                        53.524948
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 274,
                "properties": {
                    "name": "Точка: 274"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77753,
                        53.524755
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 275,
                "properties": {
                    "name": "Точка: 275"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77742,
                        53.524663
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 276,
                "properties": {
                    "name": "Точка: 276"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77736,
                        53.524547
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 277,
                "properties": {
                    "name": "Точка: 277"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7773,
                        53.52438
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 278,
                "properties": {
                    "name": "Точка: 278"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77734,
                        53.524342
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 279,
                "properties": {
                    "name": "Точка: 279"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7772,
                        53.524068
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 280,
                "properties": {
                    "name": "Точка: 280"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77657,
                        53.523596
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 281,
                "properties": {
                    "name": "Точка: 281"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77608,
                        53.523352
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 282,
                "properties": {
                    "name": "Точка: 282"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77575,
                        53.523075
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 283,
                "properties": {
                    "name": "Точка: 283"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77519,
                        53.523067
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 284,
                "properties": {
                    "name": "Точка: 284"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77437,
                        53.522511
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 285,
                "properties": {
                    "name": "Точка: 285"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77375,
                        53.522558
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 286,
                "properties": {
                    "name": "Точка: 286"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7732,
                        53.522739
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 287,
                "properties": {
                    "name": "Точка: 287"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77208,
                        53.522568
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 288,
                "properties": {
                    "name": "Точка: 288"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77142,
                        53.522631
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 289,
                "properties": {
                    "name": "Точка: 289"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.77037,
                        53.522407
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 290,
                "properties": {
                    "name": "Точка: 290"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76987,
                        53.522175
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 291,
                "properties": {
                    "name": "Точка: 291"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76952,
                        53.521904
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 292,
                "properties": {
                    "name": "Точка: 292"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76919,
                        53.521584
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 293,
                "properties": {
                    "name": "Точка: 293"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76895,
                        53.521222
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 294,
                "properties": {
                    "name": "Точка: 294"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76865,
                        53.520879
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 295,
                "properties": {
                    "name": "Точка: 295"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76858,
                        53.520505
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 296,
                "properties": {
                    "name": "Точка: 296"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76849,
                        53.520374
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 297,
                "properties": {
                    "name": "Точка: 297"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76844,
                        53.520048
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 298,
                "properties": {
                    "name": "Точка: 298"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76821,
                        53.519287
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 299,
                "properties": {
                    "name": "Точка: 299"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76803,
                        53.518914
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 300,
                "properties": {
                    "name": "Точка: 300"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76783,
                        53.517791
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 301,
                "properties": {
                    "name": "Точка: 301"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76674,
                        53.516775
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 302,
                "properties": {
                    "name": "Точка: 302"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76613,
                        53.516026
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 303,
                "properties": {
                    "name": "Точка: 303"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76588,
                        53.515618
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 304,
                "properties": {
                    "name": "Точка: 304"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7658100000001,
                        53.51522
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 305,
                "properties": {
                    "name": "Точка: 305"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76555,
                        53.514893
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 306,
                "properties": {
                    "name": "Точка: 306"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76523,
                        53.514559
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 307,
                "properties": {
                    "name": "Точка: 307"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7648200000001,
                        53.514329
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 308,
                "properties": {
                    "name": "Точка: 308"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76452,
                        53.514106
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 309,
                "properties": {
                    "name": "Точка: 309"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76397,
                        53.512926
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 310,
                "properties": {
                    "name": "Точка: 310"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76359,
                        53.51132
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 311,
                "properties": {
                    "name": "Точка: 311"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76334,
                        53.510949
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 312,
                "properties": {
                    "name": "Точка: 312"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76303,
                        53.510584
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 313,
                "properties": {
                    "name": "Точка: 313"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76262,
                        53.510295
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 314,
                "properties": {
                    "name": "Точка: 314"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76215,
                        53.510075
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 315,
                "properties": {
                    "name": "Точка: 315"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76163,
                        53.509895
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 316,
                "properties": {
                    "name": "Точка: 316"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76131,
                        53.509841
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 317,
                "properties": {
                    "name": "Точка: 317"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76103,
                        53.509855
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 318,
                "properties": {
                    "name": "Точка: 318"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76068,
                        53.510039
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 319,
                "properties": {
                    "name": "Точка: 319"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.76024,
                        53.509985
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 320,
                "properties": {
                    "name": "Точка: 320"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75998,
                        53.509776
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 321,
                "properties": {
                    "name": "Точка: 321"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75988,
                        53.509803
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 322,
                "properties": {
                    "name": "Точка: 322"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7591000000001,
                        53.508636
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 323,
                "properties": {
                    "name": "Точка: 323"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75902,
                        53.508622
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 324,
                "properties": {
                    "name": "Точка: 324"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75904,
                        53.508464
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 325,
                "properties": {
                    "name": "Точка: 325"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75899,
                        53.508166
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 326,
                "properties": {
                    "name": "Точка: 326"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75888,
                        53.508049
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 327,
                "properties": {
                    "name": "Точка: 327"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75834,
                        53.507719
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 328,
                "properties": {
                    "name": "Точка: 328"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75808,
                        53.507499
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 329,
                "properties": {
                    "name": "Точка: 329"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75778,
                        53.507199
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 330,
                "properties": {
                    "name": "Точка: 330"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7577,
                        53.507021
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 331,
                "properties": {
                    "name": "Точка: 331"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75742,
                        53.506791
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 332,
                "properties": {
                    "name": "Точка: 332"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75724,
                        53.506415
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 333,
                "properties": {
                    "name": "Точка: 333"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7573000000001,
                        53.506383
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 334,
                "properties": {
                    "name": "Точка: 334"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75722,
                        53.506373
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 335,
                "properties": {
                    "name": "Точка: 335"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7572,
                        53.506317
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 336,
                "properties": {
                    "name": "Точка: 336"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75718,
                        53.506188
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 337,
                "properties": {
                    "name": "Точка: 337"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75722,
                        53.505966
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 338,
                "properties": {
                    "name": "Точка: 338"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75718,
                        53.505831
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 339,
                "properties": {
                    "name": "Точка: 339"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75709,
                        53.505655
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 340,
                "properties": {
                    "name": "Точка: 340"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75692,
                        53.505495
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 341,
                "properties": {
                    "name": "Точка: 341"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75673,
                        53.505373
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 342,
                "properties": {
                    "name": "Точка: 342"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75616,
                        53.505286
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 343,
                "properties": {
                    "name": "Точка: 343"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75567,
                        53.505132
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 344,
                "properties": {
                    "name": "Точка: 344"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75534,
                        53.504994
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 345,
                "properties": {
                    "name": "Точка: 345"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75493,
                        53.504722
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 346,
                "properties": {
                    "name": "Точка: 346"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75467,
                        53.504715
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 347,
                "properties": {
                    "name": "Точка: 347"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7546,
                        53.504679
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 348,
                "properties": {
                    "name": "Точка: 348"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75368,
                        53.504553
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 349,
                "properties": {
                    "name": "Точка: 349"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75338,
                        53.504428
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 350,
                "properties": {
                    "name": "Точка: 350"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.753,
                        53.504353
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 351,
                "properties": {
                    "name": "Точка: 351"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75229,
                        53.504121
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 352,
                "properties": {
                    "name": "Точка: 352"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.7511300000001,
                        53.503687
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 353,
                "properties": {
                    "name": "Точка: 353"
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [
                        158.75002,
                        53.503501
                    ]
                }
            }
        ]
    },
    "context_lines_trek": {
        "type": "FeatureCollection",
        "crs": {
            "type": "name",
            "properties": {
                "name": "EPSG:4326"
            }
        },
        "features": [
            {
                "type": "Feature",
                "id": 1,
                "properties": {
                    "name": "Точка: 1 - Точка: 2",
                    "azimuth": "47 град 38 мин 11.6 с",
                    "pn": 0.0,
                    "distance": "20.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.839538,
                            53.572238
                        ],
                        [
                            158.83972,
                            53.572024
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 2,
                "properties": {
                    "name": "Точка: 2 - Точка: 3",
                    "azimuth": "84 град 28 мин 55.8 с",
                    "pn": 0.0,
                    "distance": "15.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83972,
                            53.572024
                        ],
                        [
                            158.83974,
                            53.571802
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 3,
                "properties": {
                    "name": "Точка: 3 - Точка: 4",
                    "azimuth": "144 град 45 мин 17.5 с",
                    "pn": 0.0,
                    "distance": "23.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83974,
                            53.571802
                        ],
                        [
                            158.83948,
                            53.571605
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 4,
                "properties": {
                    "name": "Точка: 4 - Точка: 5",
                    "azimuth": "64 град 37 мин 1.6 с",
                    "pn": 0.0,
                    "distance": "17.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83948,
                            53.571605
                        ],
                        [
                            158.83958,
                            53.571379
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 5,
                "properties": {
                    "name": "Точка: 5 - Точка: 6",
                    "azimuth": "47 град 38 мин 43.7 с",
                    "pn": 0.0,
                    "distance": "23.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83958,
                            53.571379
                        ],
                        [
                            158.83979,
                            53.571132
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 6,
                "properties": {
                    "name": "Точка: 6 - Точка: 7",
                    "azimuth": "69 град 2 мин 41.9 с",
                    "pn": 0.0,
                    "distance": "6.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83979,
                            53.571132
                        ],
                        [
                            158.83982,
                            53.571048
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 7,
                "properties": {
                    "name": "Точка: 7 - Точка: 8",
                    "azimuth": "33 град 54 мин 37.2 с",
                    "pn": 0.0,
                    "distance": "42.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83982,
                            53.571048
                        ],
                        [
                            158.8403,
                            53.570702
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 8,
                "properties": {
                    "name": "Точка: 8 - Точка: 9",
                    "azimuth": "67 град 22 мин 26.4 с",
                    "pn": 0.0,
                    "distance": "21.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8403,
                            53.570702
                        ],
                        [
                            158.84041,
                            53.570419
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 9,
                "properties": {
                    "name": "Точка: 9 - Точка: 10",
                    "azimuth": "129 град 47 мин 21.4 с",
                    "pn": 0.0,
                    "distance": "9.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84041,
                            53.570419
                        ],
                        [
                            158.84033,
                            53.570316
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 10,
                "properties": {
                    "name": "Точка: 10 - Точка: 11",
                    "azimuth": "30 град 34 мин 3.3 с",
                    "pn": 0.0,
                    "distance": "36.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84033,
                            53.570316
                        ],
                        [
                            158.84075,
                            53.57005
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 11,
                "properties": {
                    "name": "Точка: 11 - Точка: 12",
                    "azimuth": "38 град 26 мин 14.0 с",
                    "pn": 0.0,
                    "distance": "46.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84075,
                            53.57005
                        ],
                        [
                            158.84124,
                            53.569633
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 12,
                "properties": {
                    "name": "Точка: 12 - Точка: 13",
                    "azimuth": "81 град 51 мин 48.5 с",
                    "pn": 0.0,
                    "distance": "10.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84124,
                            53.569633
                        ],
                        [
                            158.84126,
                            53.569483
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 13,
                "properties": {
                    "name": "Точка: 13 - Точка: 14",
                    "azimuth": "117 град 36 мин 45.5 с",
                    "pn": 0.0,
                    "distance": "6.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84126,
                            53.569483
                        ],
                        [
                            158.84122,
                            53.569401
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 14,
                "properties": {
                    "name": "Точка: 14 - Точка: 15",
                    "azimuth": "90 град 0 мин 0.1 с",
                    "pn": 0.0,
                    "distance": "13.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84122,
                            53.569401
                        ],
                        [
                            158.84122,
                            53.569206
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 15,
                "properties": {
                    "name": "Точка: 15 - Точка: 16",
                    "azimuth": "84 град 19 мин 48.0 с",
                    "pn": 0.0,
                    "distance": "30.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84122,
                            53.569206
                        ],
                        [
                            158.84126,
                            53.568774
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 16,
                "properties": {
                    "name": "Точка: 16 - Точка: 17",
                    "azimuth": "160 град 53 мин 40.3 с",
                    "pn": 0.0,
                    "distance": "5.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84126,
                            53.568774
                        ],
                        [
                            158.84119,
                            53.568748
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 17,
                "properties": {
                    "name": "Точка: 17 - Точка: 18",
                    "azimuth": "94 град 49 мин 34.4 с",
                    "pn": 0.0,
                    "distance": "17.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84119,
                            53.568748
                        ],
                        [
                            158.84117,
                            53.568494
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 18,
                "properties": {
                    "name": "Точка: 18 - Точка: 19",
                    "azimuth": "84 град 32 мин 36.1 с",
                    "pn": 0.0,
                    "distance": "31.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84117,
                            53.568494
                        ],
                        [
                            158.84121,
                            53.568045
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 19,
                "properties": {
                    "name": "Точка: 19 - Точка: 20",
                    "azimuth": "109 град 40 мин 6.4 с",
                    "pn": 0.0,
                    "distance": "8.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84121,
                            53.568045
                        ],
                        [
                            158.84117,
                            53.567925
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 20,
                "properties": {
                    "name": "Точка: 20 - Точка: 21",
                    "azimuth": "70 град 55 мин 10.4 с",
                    "pn": 0.0,
                    "distance": "18.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84117,
                            53.567925
                        ],
                        [
                            158.84125,
                            53.567677
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 21,
                "properties": {
                    "name": "Точка: 21 - Точка: 22",
                    "azimuth": "95 град 50 мин 58.2 с",
                    "pn": 0.0,
                    "distance": "21.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84125,
                            53.567677
                        ],
                        [
                            158.84122,
                            53.567363
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 22,
                "properties": {
                    "name": "Точка: 22 - Точка: 23",
                    "azimuth": "54 град 26 мин 26.1 с",
                    "pn": 0.0,
                    "distance": "12.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84122,
                            53.567363
                        ],
                        [
                            158.84132,
                            53.567213
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 23,
                "properties": {
                    "name": "Точка: 23 - Точка: 24",
                    "azimuth": "72 град 57 мин 59.9 с",
                    "pn": 0.0,
                    "distance": "12.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84132,
                            53.567213
                        ],
                        [
                            158.84137,
                            53.567038
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 24,
                "properties": {
                    "name": "Точка: 24 - Точка: 25",
                    "azimuth": "82 град 40 мин 4.2 с",
                    "pn": 0.0,
                    "distance": "17.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84137,
                            53.567038
                        ],
                        [
                            158.8414,
                            53.566788
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 25,
                "properties": {
                    "name": "Точка: 25 - Точка: 26",
                    "azimuth": "103 град 36 мин 40.0 с",
                    "pn": 0.0,
                    "distance": "22.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8414,
                            53.566788
                        ],
                        [
                            158.84133,
                            53.566478
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 26,
                "properties": {
                    "name": "Точка: 26 - Точка: 27",
                    "azimuth": "63 град 6 мин 27.3 с",
                    "pn": 0.0,
                    "distance": "22.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84133,
                            53.566478
                        ],
                        [
                            158.84147,
                            53.566182
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 27,
                "properties": {
                    "name": "Точка: 27 - Точка: 28",
                    "azimuth": "93 град 21 мин 12.4 с",
                    "pn": 0.0,
                    "distance": "12.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84147,
                            53.566182
                        ],
                        [
                            158.84146,
                            53.565999
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 28,
                "properties": {
                    "name": "Точка: 28 - Точка: 29",
                    "azimuth": "75 град 36 мин 44.6 с",
                    "pn": 0.0,
                    "distance": "44.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84146,
                            53.565999
                        ],
                        [
                            158.84161,
                            53.565372
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 29,
                "properties": {
                    "name": "Точка: 29 - Точка: 30",
                    "azimuth": "97 град 21 мин 40.9 с",
                    "pn": 0.0,
                    "distance": "11.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84161,
                            53.565372
                        ],
                        [
                            158.84159,
                            53.565206
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 30,
                "properties": {
                    "name": "Точка: 30 - Точка: 31",
                    "azimuth": "68 град 30 мин 35.7 с",
                    "pn": 0.0,
                    "distance": "34.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84159,
                            53.565206
                        ],
                        [
                            158.84176,
                            53.564743
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 31,
                "properties": {
                    "name": "Точка: 31 - Точка: 32",
                    "azimuth": "116 град 16 мин 51.3 с",
                    "pn": 0.0,
                    "distance": "11.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84176,
                            53.564743
                        ],
                        [
                            158.84169,
                            53.564591
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 32,
                "properties": {
                    "name": "Точка: 32 - Точка: 33",
                    "azimuth": "149 град 18 мин 44.7 с",
                    "pn": 0.0,
                    "distance": "9.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84169,
                            53.564591
                        ],
                        [
                            158.84158,
                            53.564521
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 33,
                "properties": {
                    "name": "Точка: 33 - Точка: 34",
                    "azimuth": "97 град 58 мин 44.9 с",
                    "pn": 0.0,
                    "distance": "32.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84158,
                            53.564521
                        ],
                        [
                            158.84152,
                            53.564062
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 34,
                "properties": {
                    "name": "Точка: 34 - Точка: 35",
                    "azimuth": "116 град 37 мин 50.1 с",
                    "pn": 0.0,
                    "distance": "21.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84152,
                            53.564062
                        ],
                        [
                            158.84139,
                            53.563784
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 35,
                "properties": {
                    "name": "Точка: 35 - Точка: 36",
                    "azimuth": "147 град 52 мин 16.0 с",
                    "pn": 0.0,
                    "distance": "82.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84139,
                            53.563784
                        ],
                        [
                            158.84045,
                            53.563151
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 36,
                "properties": {
                    "name": "Точка: 36 - Точка: 37",
                    "azimuth": "129 град 1 мин 23.8 с",
                    "pn": 0.0,
                    "distance": "15.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84045,
                            53.563151
                        ],
                        [
                            158.84032,
                            53.562979
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 37,
                "properties": {
                    "name": "Точка: 37 - Точка: 38",
                    "azimuth": "153 град 37 мин 13.4 с",
                    "pn": 0.0,
                    "distance": "18.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.84032,
                            53.562979
                        ],
                        [
                            158.8401,
                            53.562862
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 38,
                "properties": {
                    "name": "Точка: 38 - Точка: 39",
                    "azimuth": "184 град 0 мин 3.4 с",
                    "pn": 0.0,
                    "distance": "11.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8401,
                            53.562862
                        ],
                        [
                            158.83994,
                            53.562874
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 39,
                "properties": {
                    "name": "Точка: 39 - Точка: 40",
                    "azimuth": "136 град 59 мин 53.6 с",
                    "pn": 0.0,
                    "distance": "25.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83994,
                            53.562874
                        ],
                        [
                            158.83969,
                            53.562624
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 40,
                "properties": {
                    "name": "Точка: 40 - Точка: 41",
                    "azimuth": "126 град 52 мин 34.2 с",
                    "pn": 0.0,
                    "distance": "21.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83969,
                            53.562624
                        ],
                        [
                            158.83952,
                            53.562381
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 41,
                "properties": {
                    "name": "Точка: 41 - Точка: 42",
                    "azimuth": "138 град 55 мин 29.1 с",
                    "pn": 0.0,
                    "distance": "25.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83952,
                            53.562381
                        ],
                        [
                            158.83926,
                            53.562138
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 42,
                "properties": {
                    "name": "Точка: 42 - Точка: 43",
                    "azimuth": "163 град 52 мин 32.2 с",
                    "pn": 0.0,
                    "distance": "23.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83926,
                            53.562138
                        ],
                        [
                            158.83896,
                            53.562045
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 43,
                "properties": {
                    "name": "Точка: 43 - Точка: 44",
                    "azimuth": "154 град 0 мин 42.3 с",
                    "pn": 0.0,
                    "distance": "18.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83896,
                            53.562045
                        ],
                        [
                            158.83874,
                            53.56193
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 44,
                "properties": {
                    "name": "Точка: 44 - Точка: 45",
                    "azimuth": "132 град 25 мин 27.1 с",
                    "pn": 0.0,
                    "distance": "16.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83874,
                            53.56193
                        ],
                        [
                            158.83859,
                            53.561754
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 45,
                "properties": {
                    "name": "Точка: 45 - Точка: 46",
                    "azimuth": "162 град 6 мин 33.6 с",
                    "pn": 0.0,
                    "distance": "10.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83859,
                            53.561754
                        ],
                        [
                            158.83846,
                            53.561709
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 46,
                "properties": {
                    "name": "Точка: 46 - Точка: 47",
                    "azimuth": "137 град 13 мин 8.7 с",
                    "pn": 0.0,
                    "distance": "13.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83846,
                            53.561709
                        ],
                        [
                            158.83833,
                            53.56158
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 47,
                "properties": {
                    "name": "Точка: 47 - Точка: 48",
                    "azimuth": "126 град 48 мин 4.0 с",
                    "pn": 0.0,
                    "distance": "26.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83833,
                            53.56158
                        ],
                        [
                            158.83812,
                            53.561279
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 48,
                "properties": {
                    "name": "Точка: 48 - Точка: 49",
                    "azimuth": "148 град 7 мин 49.5 с",
                    "pn": 0.0,
                    "distance": "13.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83812,
                            53.561279
                        ],
                        [
                            158.83797,
                            53.561179
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 49,
                "properties": {
                    "name": "Точка: 49 - Точка: 50",
                    "azimuth": "111 град 46 мин 57.6 с",
                    "pn": 0.0,
                    "distance": "12.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83797,
                            53.561179
                        ],
                        [
                            158.83791,
                            53.561018
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 50,
                "properties": {
                    "name": "Точка: 50 - Точка: 51",
                    "azimuth": "138 град 44 мин 4.2 с",
                    "pn": 0.0,
                    "distance": "21.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83791,
                            53.561018
                        ],
                        [
                            158.83769,
                            53.560811
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 51,
                "properties": {
                    "name": "Точка: 51 - Точка: 52",
                    "azimuth": "114 град 40 мин 54.5 с",
                    "pn": 0.0,
                    "distance": "5.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83769,
                            53.560811
                        ],
                        [
                            158.83766,
                            53.560741
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 52,
                "properties": {
                    "name": "Точка: 52 - Точка: 53",
                    "azimuth": "151 град 35 мин 30.2 с",
                    "pn": 0.0,
                    "distance": "12.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83766,
                            53.560741
                        ],
                        [
                            158.83751,
                            53.560654
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 53,
                "properties": {
                    "name": "Точка: 53 - Точка: 54",
                    "azimuth": "135 град 9 мин 4.9 с",
                    "pn": 0.0,
                    "distance": "9.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83751,
                            53.560654
                        ],
                        [
                            158.83742,
                            53.560558
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 54,
                "properties": {
                    "name": "Точка: 54 - Точка: 55",
                    "azimuth": "157 град 0 мин 28.1 с",
                    "pn": 0.0,
                    "distance": "16.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83742,
                            53.560558
                        ],
                        [
                            158.83722,
                            53.560467
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 55,
                "properties": {
                    "name": "Точка: 55 - Точка: 56",
                    "azimuth": "137 град 35 мин 59.9 с",
                    "pn": 0.0,
                    "distance": "48.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83722,
                            53.560467
                        ],
                        [
                            158.83674,
                            53.559997
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 56,
                "properties": {
                    "name": "Точка: 56 - Точка: 57",
                    "azimuth": "154 град 51 мин 1.1 с",
                    "pn": 0.0,
                    "distance": "23.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83674,
                            53.559997
                        ],
                        [
                            158.83645,
                            53.559851
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 57,
                "properties": {
                    "name": "Точка: 57 - Точка: 58",
                    "azimuth": "162 град 54 мин 28.3 с",
                    "pn": 0.0,
                    "distance": "28.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83645,
                            53.559851
                        ],
                        [
                            158.83608,
                            53.559729
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 58,
                "properties": {
                    "name": "Точка: 58 - Точка: 59",
                    "azimuth": "148 град 12 мин 23.1 с",
                    "pn": 0.0,
                    "distance": "14.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83608,
                            53.559729
                        ],
                        [
                            158.83591,
                            53.559616
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 59,
                "properties": {
                    "name": "Точка: 59 - Точка: 60",
                    "azimuth": "176 град 41 мин 14.2 с",
                    "pn": 0.0,
                    "distance": "21.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83591,
                            53.559616
                        ],
                        [
                            158.83562,
                            53.559598
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 60,
                "properties": {
                    "name": "Точка: 60 - Точка: 61",
                    "azimuth": "156 град 19 мин 56.4 с",
                    "pn": 0.0,
                    "distance": "40.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83562,
                            53.559598
                        ],
                        [
                            158.83512,
                            53.559363
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 61,
                "properties": {
                    "name": "Точка: 61 - Точка: 62",
                    "azimuth": "147 град 45 мин 55.5 с",
                    "pn": 0.0,
                    "distance": "18.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83512,
                            53.559363
                        ],
                        [
                            158.83491,
                            53.559221
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 62,
                "properties": {
                    "name": "Точка: 62 - Точка: 63",
                    "azimuth": "162 град 50 мин 1.8 с",
                    "pn": 0.0,
                    "distance": "12.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83491,
                            53.559221
                        ],
                        [
                            158.83475,
                            53.559168
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 63,
                "properties": {
                    "name": "Точка: 63 - Точка: 64",
                    "azimuth": "118 град 48 мин 25.9 с",
                    "pn": 0.0,
                    "distance": "30.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83475,
                            53.559168
                        ],
                        [
                            158.83455,
                            53.558778
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 64,
                "properties": {
                    "name": "Точка: 64 - Точка: 65",
                    "azimuth": "138 град 12 мин 48.0 с",
                    "pn": 0.0,
                    "distance": "11.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83455,
                            53.558778
                        ],
                        [
                            158.83443,
                            53.558663
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 65,
                "properties": {
                    "name": "Точка: 65 - Точка: 66",
                    "azimuth": "150 град 46 мин 19.0 с",
                    "pn": 0.0,
                    "distance": "17.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83443,
                            53.558663
                        ],
                        [
                            158.83423,
                            53.558543
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 66,
                "properties": {
                    "name": "Точка: 66 - Точка: 67",
                    "azimuth": "135 град 36 мин 11.4 с",
                    "pn": 0.0,
                    "distance": "27.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83423,
                            53.558543
                        ],
                        [
                            158.83397,
                            53.55827
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 67,
                "properties": {
                    "name": "Точка: 67 - Точка: 68",
                    "azimuth": "109 град 25 мин 48.1 с",
                    "pn": 0.0,
                    "distance": "11.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83397,
                            53.55827
                        ],
                        [
                            158.83392,
                            53.558118
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 68,
                "properties": {
                    "name": "Точка: 68 - Точка: 69",
                    "azimuth": "94 град 50 мин 43.6 с",
                    "pn": 0.0,
                    "distance": "17.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83392,
                            53.558118
                        ],
                        [
                            158.8339,
                            53.557865
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 69,
                "properties": {
                    "name": "Точка: 69 - Точка: 70",
                    "azimuth": "113 град 55 мин 41.8 с",
                    "pn": 0.0,
                    "distance": "21.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8339,
                            53.557865
                        ],
                        [
                            158.83378,
                            53.557575
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 70,
                "properties": {
                    "name": "Точка: 70 - Точка: 71",
                    "azimuth": "145 град 5 мин 34.6 с",
                    "pn": 0.0,
                    "distance": "26.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83378,
                            53.557575
                        ],
                        [
                            158.83349,
                            53.557358
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 71,
                "properties": {
                    "name": "Точка: 71 - Точка: 72",
                    "azimuth": "128 град 30 мин 9.5 с",
                    "pn": 0.0,
                    "distance": "29.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83349,
                            53.557358
                        ],
                        [
                            158.83324,
                            53.557021
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 72,
                "properties": {
                    "name": "Точка: 72 - Точка: 73",
                    "azimuth": "144 град 55 мин 32.5 с",
                    "pn": 0.0,
                    "distance": "15.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83324,
                            53.557021
                        ],
                        [
                            158.83307,
                            53.556893
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 73,
                "properties": {
                    "name": "Точка: 73 - Точка: 74",
                    "azimuth": "155 град 48 мин 18.5 с",
                    "pn": 0.0,
                    "distance": "26.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83307,
                            53.556893
                        ],
                        [
                            158.83274,
                            53.556734
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 74,
                "properties": {
                    "name": "Точка: 74 - Точка: 75",
                    "azimuth": "160 град 22 мин 16.3 с",
                    "pn": 0.0,
                    "distance": "44.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83274,
                            53.556734
                        ],
                        [
                            158.83217,
                            53.556516
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 75,
                "properties": {
                    "name": "Точка: 75 - Точка: 76",
                    "azimuth": "141 град 47 мин 29.8 с",
                    "pn": 0.0,
                    "distance": "32.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83217,
                            53.556516
                        ],
                        [
                            158.83183,
                            53.556229
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 76,
                "properties": {
                    "name": "Точка: 76 - Точка: 77",
                    "azimuth": "159 град 1 мин 29.0 с",
                    "pn": 0.0,
                    "distance": "64.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83183,
                            53.556229
                        ],
                        [
                            158.83102,
                            53.555896
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 77,
                "properties": {
                    "name": "Точка: 77 - Точка: 78",
                    "azimuth": "184 град 21 мин 47.0 с",
                    "pn": 0.0,
                    "distance": "8.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83102,
                            53.555896
                        ],
                        [
                            158.83091,
                            53.555905
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 78,
                "properties": {
                    "name": "Точка: 78 - Точка: 79",
                    "azimuth": "168 град 50 мин 54.5 с",
                    "pn": 0.0,
                    "distance": "59.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83091,
                            53.555905
                        ],
                        [
                            158.83012,
                            53.555738
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 79,
                "properties": {
                    "name": "Точка: 79 - Точка: 80",
                    "azimuth": "181 град 20 мин 7.7 с",
                    "pn": 0.0,
                    "distance": "23.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.83012,
                            53.555738
                        ],
                        [
                            158.8298,
                            53.555746
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 80,
                "properties": {
                    "name": "Точка: 80 - Точка: 81",
                    "azimuth": "174 град 12 мин 19.9 с",
                    "pn": 0.0,
                    "distance": "25.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8298,
                            53.555746
                        ],
                        [
                            158.82946,
                            53.555709
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 81,
                "properties": {
                    "name": "Точка: 81 - Точка: 82",
                    "azimuth": "155 град 59 мин 52.5 с",
                    "pn": 0.0,
                    "distance": "32.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82946,
                            53.555709
                        ],
                        [
                            158.82906,
                            53.555518
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 82,
                "properties": {
                    "name": "Точка: 82 - Точка: 83",
                    "azimuth": "165 град 4 мин 52.4 с",
                    "pn": 0.0,
                    "distance": "16.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82906,
                            53.555518
                        ],
                        [
                            158.8288500000001,
                            53.555458
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 83,
                "properties": {
                    "name": "Точка: 83 - Точка: 84",
                    "azimuth": "191 град 4 мин 47.2 с",
                    "pn": 0.0,
                    "distance": "22.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8288500000001,
                            53.555458
                        ],
                        [
                            158.82855,
                            53.555521
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 84,
                "properties": {
                    "name": "Точка: 84 - Точка: 85",
                    "azimuth": "170 град 55 мин 3.7 с",
                    "pn": 0.0,
                    "distance": "21.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82855,
                            53.555521
                        ],
                        [
                            158.82827,
                            53.555473
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 85,
                "properties": {
                    "name": "Точка: 85 - Точка: 86",
                    "azimuth": "182 град 31 мин 45.0 с",
                    "pn": 0.0,
                    "distance": "14.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82827,
                            53.555473
                        ],
                        [
                            158.82808,
                            53.555482
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 86,
                "properties": {
                    "name": "Точка: 86 - Точка: 87",
                    "azimuth": "168 град 28 мин 14.8 с",
                    "pn": 0.0,
                    "distance": "48.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82808,
                            53.555482
                        ],
                        [
                            158.82744,
                            53.555342
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 87,
                "properties": {
                    "name": "Точка: 87 - Точка: 88",
                    "azimuth": "155 град 46 мин 55.8 с",
                    "pn": 0.0,
                    "distance": "13.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82744,
                            53.555342
                        ],
                        [
                            158.82727,
                            53.55526
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 88,
                "properties": {
                    "name": "Точка: 88 - Точка: 89",
                    "azimuth": "169 град 11 мин 24.3 с",
                    "pn": 0.0,
                    "distance": "15.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82727,
                            53.55526
                        ],
                        [
                            158.82706,
                            53.555217
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 89,
                "properties": {
                    "name": "Точка: 89 - Точка: 90",
                    "azimuth": "183 град 22 мин 13.8 с",
                    "pn": 0.0,
                    "distance": "14.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82706,
                            53.555217
                        ],
                        [
                            158.82687,
                            53.555229
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 90,
                "properties": {
                    "name": "Точка: 90 - Точка: 91",
                    "azimuth": "171 град 1 мин 56.3 с",
                    "pn": 0.0,
                    "distance": "19.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82687,
                            53.555229
                        ],
                        [
                            158.82661,
                            53.555185
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 91,
                "properties": {
                    "name": "Точка: 91 - Точка: 92",
                    "azimuth": "177 град 55 мин 50.1 с",
                    "pn": 0.0,
                    "distance": "59.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82661,
                            53.555185
                        ],
                        [
                            158.82581,
                            53.555154
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 92,
                "properties": {
                    "name": "Точка: 92 - Точка: 93",
                    "azimuth": "172 град 38 мин 9.5 с",
                    "pn": 0.0,
                    "distance": "42.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82581,
                            53.555154
                        ],
                        [
                            158.82524,
                            53.555075
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 93,
                "properties": {
                    "name": "Точка: 93 - Точка: 94",
                    "azimuth": "159 град 16 мин 10.0 с",
                    "pn": 0.0,
                    "distance": "13.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82524,
                            53.555075
                        ],
                        [
                            158.82507,
                            53.555006
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 94,
                "properties": {
                    "name": "Точка: 94 - Точка: 95",
                    "azimuth": "178 град 1 мин 19.2 с",
                    "pn": 0.0,
                    "distance": "40.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82507,
                            53.555006
                        ],
                        [
                            158.82453,
                            53.554986
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 95,
                "properties": {
                    "name": "Точка: 95 - Точка: 96",
                    "azimuth": "171 град 8 мин 55.8 с",
                    "pn": 0.0,
                    "distance": "75.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82453,
                            53.554986
                        ],
                        [
                            158.82353,
                            53.554819
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 96,
                "properties": {
                    "name": "Точка: 96 - Точка: 97",
                    "azimuth": "148 град 46 мин 47.1 с",
                    "pn": 0.0,
                    "distance": "45.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82353,
                            53.554819
                        ],
                        [
                            158.82301,
                            53.554481
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 97,
                "properties": {
                    "name": "Точка: 97 - Точка: 98",
                    "azimuth": "165 град 43 мин 53.8 с",
                    "pn": 0.0,
                    "distance": "8.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82301,
                            53.554481
                        ],
                        [
                            158.8229,
                            53.554451
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 98,
                "properties": {
                    "name": "Точка: 98 - Точка: 99",
                    "azimuth": "128 град 40 мин 15.1 с",
                    "pn": 0.0,
                    "distance": "17.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8229,
                            53.554451
                        ],
                        [
                            158.82275,
                            53.55425
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 99,
                "properties": {
                    "name": "Точка: 99 - Точка: 100",
                    "azimuth": "142 град 11 мин 0.8 с",
                    "pn": 0.0,
                    "distance": "31.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82275,
                            53.55425
                        ],
                        [
                            158.82241,
                            53.553967
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 100,
                "properties": {
                    "name": "Точка: 100 - Точка: 101",
                    "azimuth": "127 град 48 мин 54.0 с",
                    "pn": 0.0,
                    "distance": "13.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82241,
                            53.553967
                        ],
                        [
                            158.8223,
                            53.553815
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 101,
                "properties": {
                    "name": "Точка: 101 - Точка: 102",
                    "azimuth": "150 град 46 мин 26.3 с",
                    "pn": 0.0,
                    "distance": "19.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8223,
                            53.553815
                        ],
                        [
                            158.82207,
                            53.553677
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 102,
                "properties": {
                    "name": "Точка: 102 - Точка: 103",
                    "azimuth": "169 град 57 мин 11.8 с",
                    "pn": 0.0,
                    "distance": "7.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82207,
                            53.553677
                        ],
                        [
                            158.82197,
                            53.553658
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 103,
                "properties": {
                    "name": "Точка: 103 - Точка: 104",
                    "azimuth": "145 град 17 мин 24.8 с",
                    "pn": 0.0,
                    "distance": "12.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82197,
                            53.553658
                        ],
                        [
                            158.82183,
                            53.553554
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 104,
                "properties": {
                    "name": "Точка: 104 - Точка: 105",
                    "azimuth": "112 град 48 мин 35.1 с",
                    "pn": 0.0,
                    "distance": "7.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82183,
                            53.553554
                        ],
                        [
                            158.82179,
                            53.553452
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 105,
                "properties": {
                    "name": "Точка: 105 - Точка: 106",
                    "azimuth": "171 град 9 мин 58.8 с",
                    "pn": 0.0,
                    "distance": "20.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82179,
                            53.553452
                        ],
                        [
                            158.82152,
                            53.553407
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 106,
                "properties": {
                    "name": "Точка: 106 - Точка: 107",
                    "azimuth": "3 град 12 мин 8.0 с",
                    "pn": 0.0,
                    "distance": "7.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82152,
                            53.553407
                        ],
                        [
                            158.82162,
                            53.553401
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 107,
                "properties": {
                    "name": "Точка: 107 - Точка: 108",
                    "azimuth": "134 град 55 мин 53.4 с",
                    "pn": 0.0,
                    "distance": "4.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82162,
                            53.553401
                        ],
                        [
                            158.82158,
                            53.553358
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 108,
                "properties": {
                    "name": "Точка: 108 - Точка: 109",
                    "azimuth": "96 град 52 мин 15.3 с",
                    "pn": 0.0,
                    "distance": "6.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82158,
                            53.553358
                        ],
                        [
                            158.82157,
                            53.553269
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 109,
                "properties": {
                    "name": "Точка: 109 - Точка: 110",
                    "azimuth": "132 град 4 мин 3.5 с",
                    "pn": 0.0,
                    "distance": "18.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82157,
                            53.553269
                        ],
                        [
                            158.8214,
                            53.553067
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 110,
                "properties": {
                    "name": "Точка: 110 - Точка: 111",
                    "azimuth": "151 град 44 мин 25.7 с",
                    "pn": 0.0,
                    "distance": "28.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8214,
                            53.553067
                        ],
                        [
                            158.8210600000001,
                            53.552871
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 111,
                "properties": {
                    "name": "Точка: 111 - Точка: 112",
                    "azimuth": "158 град 16 мин 37.4 с",
                    "pn": 0.0,
                    "distance": "26.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8210600000001,
                            53.552871
                        ],
                        [
                            158.82073,
                            53.55273
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 112,
                "properties": {
                    "name": "Точка: 112 - Точка: 113",
                    "azimuth": "163 град 5 мин 25.8 с",
                    "pn": 0.0,
                    "distance": "56.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82073,
                            53.55273
                        ],
                        [
                            158.82,
                            53.552492
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 113,
                "properties": {
                    "name": "Точка: 113 - Точка: 114",
                    "azimuth": "175 град 59 мин 58.6 с",
                    "pn": 0.0,
                    "distance": "17.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.82,
                            53.552492
                        ],
                        [
                            158.81976,
                            53.552474
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 114,
                "properties": {
                    "name": "Точка: 114 - Точка: 115",
                    "azimuth": "168 град 16 мин 3.2 с",
                    "pn": 0.0,
                    "distance": "50.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81976,
                            53.552474
                        ],
                        [
                            158.8191,
                            53.552327
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 115,
                "properties": {
                    "name": "Точка: 115 - Точка: 116",
                    "azimuth": "166 град 10 мин 3.5 с",
                    "pn": 0.0,
                    "distance": "48.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8191,
                            53.552327
                        ],
                        [
                            158.81846,
                            53.552158
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 116,
                "properties": {
                    "name": "Точка: 116 - Точка: 117",
                    "azimuth": "157 град 3 мин 45.8 с",
                    "pn": 0.0,
                    "distance": "31.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81846,
                            53.552158
                        ],
                        [
                            158.81807,
                            53.551981
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 117,
                "properties": {
                    "name": "Точка: 117 - Точка: 118",
                    "azimuth": "167 град 39 мин 49.6 с",
                    "pn": 0.0,
                    "distance": "83.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81807,
                            53.551981
                        ],
                        [
                            158.81697,
                            53.551723
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 118,
                "properties": {
                    "name": "Точка: 118 - Точка: 119",
                    "azimuth": "159 град 41 мин 2.7 с",
                    "pn": 0.0,
                    "distance": "80.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81697,
                            53.551723
                        ],
                        [
                            158.81595,
                            53.551318
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 119,
                "properties": {
                    "name": "Точка: 119 - Точка: 120",
                    "azimuth": "165 град 10 мин 55.2 с",
                    "pn": 0.0,
                    "distance": "33.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81595,
                            53.551318
                        ],
                        [
                            158.81552,
                            53.551196
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 120,
                "properties": {
                    "name": "Точка: 120 - Точка: 121",
                    "azimuth": "169 град 58 мин 31.3 с",
                    "pn": 0.0,
                    "distance": "72.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81552,
                            53.551196
                        ],
                        [
                            158.81456,
                            53.551014
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 121,
                "properties": {
                    "name": "Точка: 121 - Точка: 122",
                    "azimuth": "156 град 52 мин 20.7 с",
                    "pn": 0.0,
                    "distance": "25.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81456,
                            53.551014
                        ],
                        [
                            158.81425,
                            53.550872
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 122,
                "properties": {
                    "name": "Точка: 122 - Точка: 123",
                    "azimuth": "171 град 6 мин 16.9 с",
                    "pn": 0.0,
                    "distance": "21.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81425,
                            53.550872
                        ],
                        [
                            158.81397,
                            53.550825
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 123,
                "properties": {
                    "name": "Точка: 123 - Точка: 124",
                    "azimuth": "148 град 23 мин 32.1 с",
                    "pn": 0.0,
                    "distance": "17.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81397,
                            53.550825
                        ],
                        [
                            158.81377,
                            53.550693
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 124,
                "properties": {
                    "name": "Точка: 124 - Точка: 125",
                    "azimuth": "167 град 39 мин 23.5 с",
                    "pn": 0.0,
                    "distance": "37.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81377,
                            53.550693
                        ],
                        [
                            158.81328,
                            53.550578
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 125,
                "properties": {
                    "name": "Точка: 125 - Точка: 126",
                    "azimuth": "156 град 55 мин 37.0 с",
                    "pn": 0.0,
                    "distance": "41.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81328,
                            53.550578
                        ],
                        [
                            158.81277,
                            53.550345
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 126,
                "properties": {
                    "name": "Точка: 126 - Точка: 127",
                    "azimuth": "162 град 15 мин 40.7 с",
                    "pn": 0.0,
                    "distance": "50.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81277,
                            53.550345
                        ],
                        [
                            158.81212,
                            53.550122
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 127,
                "properties": {
                    "name": "Точка: 127 - Точка: 128",
                    "azimuth": "171 град 1 мин 10.7 с",
                    "pn": 0.0,
                    "distance": "44.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81212,
                            53.550122
                        ],
                        [
                            158.81153,
                            53.550022
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 128,
                "properties": {
                    "name": "Точка: 128 - Точка: 129",
                    "azimuth": "162 град 33 мин 22.1 с",
                    "pn": 0.0,
                    "distance": "98.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81153,
                            53.550022
                        ],
                        [
                            158.81026,
                            53.549594
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 129,
                "properties": {
                    "name": "Точка: 129 - Точка: 130",
                    "azimuth": "95 град 23 мин 25.1 с",
                    "pn": 0.0,
                    "distance": "23.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81026,
                            53.549594
                        ],
                        [
                            158.81023,
                            53.549253
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 130,
                "properties": {
                    "name": "Точка: 130 - Точка: 131",
                    "azimuth": "36 град 8 мин 35.9 с",
                    "pn": 0.0,
                    "distance": "5.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81023,
                            53.549253
                        ],
                        [
                            158.81029,
                            53.549206
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 131,
                "properties": {
                    "name": "Точка: 131 - Точка: 132",
                    "azimuth": "146 град 34 мин 53.1 с",
                    "pn": 0.0,
                    "distance": "11.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81029,
                            53.549206
                        ],
                        [
                            158.81016,
                            53.549114
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 132,
                "properties": {
                    "name": "Точка: 132 - Точка: 133",
                    "azimuth": "126 град 40 мин 43.9 с",
                    "pn": 0.0,
                    "distance": "12.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81016,
                            53.549114
                        ],
                        [
                            158.81006,
                            53.54897
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 133,
                "properties": {
                    "name": "Точка: 133 - Точка: 134",
                    "azimuth": "90 град 0 мин 0.1 с",
                    "pn": 0.0,
                    "distance": "5.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81006,
                            53.54897
                        ],
                        [
                            158.81006,
                            53.548887
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 134,
                "properties": {
                    "name": "Точка: 134 - Точка: 135",
                    "azimuth": "159 град 50 мин 42.7 с",
                    "pn": 0.0,
                    "distance": "49.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81006,
                            53.548887
                        ],
                        [
                            158.80943,
                            53.548639
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 135,
                "properties": {
                    "name": "Точка: 135 - Точка: 136",
                    "azimuth": "145 град 56 мин 31.9 с",
                    "pn": 0.0,
                    "distance": "10.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80943,
                            53.548639
                        ],
                        [
                            158.80931,
                            53.548552
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 136,
                "properties": {
                    "name": "Точка: 136 - Точка: 137",
                    "azimuth": "115 град 8 мин 14.3 с",
                    "pn": 0.0,
                    "distance": "12.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80931,
                            53.548552
                        ],
                        [
                            158.80924,
                            53.548392
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 137,
                "properties": {
                    "name": "Точка: 137 - Точка: 138",
                    "azimuth": "49 град 59 мин 28.1 с",
                    "pn": 0.0,
                    "distance": "20.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80924,
                            53.548392
                        ],
                        [
                            158.80942,
                            53.548162
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 138,
                "properties": {
                    "name": "Точка: 138 - Точка: 139",
                    "azimuth": "23 град 39 мин 50.5 с",
                    "pn": 0.0,
                    "distance": "8.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80942,
                            53.548162
                        ],
                        [
                            158.80952,
                            53.548115
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 139,
                "properties": {
                    "name": "Точка: 139 - Точка: 140",
                    "azimuth": "41 град 20 мин 15.5 с",
                    "pn": 0.0,
                    "distance": "22.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80952,
                            53.548115
                        ],
                        [
                            158.80975,
                            53.547898
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 140,
                "properties": {
                    "name": "Точка: 140 - Точка: 141",
                    "azimuth": "86 град 25 мин 55.0 с",
                    "pn": 0.0,
                    "distance": "11.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80975,
                            53.547898
                        ],
                        [
                            158.80976,
                            53.547726
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 141,
                "properties": {
                    "name": "Точка: 141 - Точка: 142",
                    "azimuth": "71 град 4 мин 39.4 с",
                    "pn": 0.0,
                    "distance": "16.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80976,
                            53.547726
                        ],
                        [
                            158.80983,
                            53.547507
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 142,
                "properties": {
                    "name": "Точка: 142 - Точка: 143",
                    "azimuth": "41 град 26 мин 0.8 с",
                    "pn": 0.0,
                    "distance": "14.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80983,
                            53.547507
                        ],
                        [
                            158.80998,
                            53.547365
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 143,
                "properties": {
                    "name": "Точка: 143 - Точка: 144",
                    "azimuth": "54 град 4 мин 12.8 с",
                    "pn": 0.0,
                    "distance": "18.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80998,
                            53.547365
                        ],
                        [
                            158.81013,
                            53.547143
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 144,
                "properties": {
                    "name": "Точка: 144 - Точка: 145",
                    "azimuth": "99 град 58 мин 19.0 с",
                    "pn": 0.0,
                    "distance": "4.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81013,
                            53.547143
                        ],
                        [
                            158.81012,
                            53.547082
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 145,
                "properties": {
                    "name": "Точка: 145 - Точка: 146",
                    "azimuth": "64 град 6 мин 45.9 с",
                    "pn": 0.0,
                    "distance": "34.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81012,
                            53.547082
                        ],
                        [
                            158.81032,
                            53.54664
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 146,
                "properties": {
                    "name": "Точка: 146 - Точка: 147",
                    "azimuth": "57 град 37 мин 18.7 с",
                    "pn": 0.0,
                    "distance": "48.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81032,
                            53.54664
                        ],
                        [
                            158.81067,
                            53.546048
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 147,
                "properties": {
                    "name": "Точка: 147 - Точка: 148",
                    "azimuth": "64 град 59 мин 59.9 с",
                    "pn": 0.0,
                    "distance": "19.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81067,
                            53.546048
                        ],
                        [
                            158.81078,
                            53.545795
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 148,
                "properties": {
                    "name": "Точка: 148 - Точка: 149",
                    "azimuth": "40 град 43 мин 31.9 с",
                    "pn": 0.0,
                    "distance": "29.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81078,
                            53.545795
                        ],
                        [
                            158.81108,
                            53.545518
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 149,
                "properties": {
                    "name": "Точка: 149 - Точка: 150",
                    "azimuth": "81 град 18 мин 16.3 с",
                    "pn": 0.0,
                    "distance": "39.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81108,
                            53.545518
                        ],
                        [
                            158.81116,
                            53.544957
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 150,
                "properties": {
                    "name": "Точка: 150 - Точка: 151",
                    "azimuth": "104 град 39 мин 33.9 с",
                    "pn": 0.0,
                    "distance": "20.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81116,
                            53.544957
                        ],
                        [
                            158.81109,
                            53.54467
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 151,
                "properties": {
                    "name": "Точка: 151 - Точка: 152",
                    "azimuth": "79 град 39 мин 46.7 с",
                    "pn": 0.0,
                    "distance": "20.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81109,
                            53.54467
                        ],
                        [
                            158.81114,
                            53.544376
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 152,
                "properties": {
                    "name": "Точка: 152 - Точка: 153",
                    "azimuth": "124 град 50 мин 37.9 с",
                    "pn": 0.0,
                    "distance": "41.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81114,
                            53.544376
                        ],
                        [
                            158.81082,
                            53.543883
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 153,
                "properties": {
                    "name": "Точка: 153 - Точка: 154",
                    "azimuth": "95 град 30 мин 9.3 с",
                    "pn": 0.0,
                    "distance": "23.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81082,
                            53.543883
                        ],
                        [
                            158.81079,
                            53.543549
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 154,
                "properties": {
                    "name": "Точка: 154 - Точка: 155",
                    "azimuth": "118 град 3 мин 36.9 с",
                    "pn": 0.0,
                    "distance": "39.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81079,
                            53.543549
                        ],
                        [
                            158.81054,
                            53.543046
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 155,
                "properties": {
                    "name": "Точка: 155 - Точка: 156",
                    "azimuth": "69 град 14 мин 5.2 с",
                    "pn": 0.0,
                    "distance": "14.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81054,
                            53.543046
                        ],
                        [
                            158.81061,
                            53.542848
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 156,
                "properties": {
                    "name": "Точка: 156 - Точка: 157",
                    "azimuth": "96 град 50 мин 0.3 с",
                    "pn": 0.0,
                    "distance": "12.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81061,
                            53.542848
                        ],
                        [
                            158.81059,
                            53.542669
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 157,
                "properties": {
                    "name": "Точка: 157 - Точка: 158",
                    "azimuth": "123 град 6 мин 45.3 с",
                    "pn": 0.0,
                    "distance": "24.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81059,
                            53.542669
                        ],
                        [
                            158.81041,
                            53.542373
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 158,
                "properties": {
                    "name": "Точка: 158 - Точка: 159",
                    "azimuth": "139 град 2 мин 50.3 с",
                    "pn": 0.0,
                    "distance": "12.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81041,
                            53.542373
                        ],
                        [
                            158.81028,
                            53.542252
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 159,
                "properties": {
                    "name": "Точка: 159 - Точка: 160",
                    "azimuth": "118 град 17 мин 7.4 с",
                    "pn": 0.0,
                    "distance": "45.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.81028,
                            53.542252
                        ],
                        [
                            158.80999,
                            53.541674
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 160,
                "properties": {
                    "name": "Точка: 160 - Точка: 161",
                    "azimuth": "90 град 0 мин 0.1 с",
                    "pn": 0.0,
                    "distance": "5.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80999,
                            53.541674
                        ],
                        [
                            158.80999,
                            53.541594
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 161,
                "properties": {
                    "name": "Точка: 161 - Точка: 162",
                    "azimuth": "130 град 37 мин 48.1 с",
                    "pn": 0.0,
                    "distance": "6.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80999,
                            53.541594
                        ],
                        [
                            158.80993,
                            53.541519
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 162,
                "properties": {
                    "name": "Точка: 162 - Точка: 163",
                    "azimuth": "105 град 22 мин 35.4 с",
                    "pn": 0.0,
                    "distance": "11.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80993,
                            53.541519
                        ],
                        [
                            158.80989,
                            53.541363
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 163,
                "properties": {
                    "name": "Точка: 163 - Точка: 164",
                    "azimuth": "142 град 25 мин 54.7 с",
                    "pn": 0.0,
                    "distance": "11.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80989,
                            53.541363
                        ],
                        [
                            158.80977,
                            53.541264
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 164,
                "properties": {
                    "name": "Точка: 164 - Точка: 165",
                    "azimuth": "99 град 20 мин 58.0 с",
                    "pn": 0.0,
                    "distance": "31.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80977,
                            53.541264
                        ],
                        [
                            158.8097,
                            53.540808
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 165,
                "properties": {
                    "name": "Точка: 165 - Точка: 166",
                    "azimuth": "116 град 18 мин 32.1 с",
                    "pn": 0.0,
                    "distance": "21.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8097,
                            53.540808
                        ],
                        [
                            158.80957,
                            53.540526
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 166,
                "properties": {
                    "name": "Точка: 166 - Точка: 167",
                    "azimuth": "94 град 32 мин 32.6 с",
                    "pn": 0.0,
                    "distance": "9.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80957,
                            53.540526
                        ],
                        [
                            158.80956,
                            53.540391
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 167,
                "properties": {
                    "name": "Точка: 167 - Точка: 168",
                    "azimuth": "113 град 13 мин 11.1 с",
                    "pn": 0.0,
                    "distance": "13.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80956,
                            53.540391
                        ],
                        [
                            158.80949,
                            53.540216
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 168,
                "properties": {
                    "name": "Точка: 168 - Точка: 169",
                    "azimuth": "127 град 27 мин 18.8 с",
                    "pn": 0.0,
                    "distance": "9.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80949,
                            53.540216
                        ],
                        [
                            158.80941,
                            53.540104
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 169,
                "properties": {
                    "name": "Точка: 169 - Точка: 170",
                    "azimuth": "162 град 41 мин 3.7 с",
                    "pn": 0.0,
                    "distance": "24.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80941,
                            53.540104
                        ],
                        [
                            158.80909,
                            53.539997
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 170,
                "properties": {
                    "name": "Точка: 170 - Точка: 171",
                    "azimuth": "173 град 26 мин 11.2 с",
                    "pn": 0.0,
                    "distance": "35.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80909,
                            53.539997
                        ],
                        [
                            158.80862,
                            53.539939
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 171,
                "properties": {
                    "name": "Точка: 171 - Точка: 172",
                    "azimuth": "148 град 53 мин 50.4 с",
                    "pn": 0.0,
                    "distance": "29.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80862,
                            53.539939
                        ],
                        [
                            158.80828,
                            53.539719
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 172,
                "properties": {
                    "name": "Точка: 172 - Точка: 173",
                    "azimuth": "155 град 35 мин 37.0 с",
                    "pn": 0.0,
                    "distance": "36.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80828,
                            53.539719
                        ],
                        [
                            158.80783,
                            53.5395
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 173,
                "properties": {
                    "name": "Точка: 173 - Точка: 174",
                    "azimuth": "178 град 54 мин 26.8 с",
                    "pn": 0.0,
                    "distance": "32.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80783,
                            53.5395
                        ],
                        [
                            158.80739,
                            53.539491
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 174,
                "properties": {
                    "name": "Точка: 174 - Точка: 175",
                    "azimuth": "185 град 50 мин 19.5 с",
                    "pn": 0.0,
                    "distance": "23.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80739,
                            53.539491
                        ],
                        [
                            158.80708,
                            53.539525
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 175,
                "properties": {
                    "name": "Точка: 175 - Точка: 176",
                    "azimuth": "166 град 59 мин 59.3 с",
                    "pn": 0.0,
                    "distance": "16.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80708,
                            53.539525
                        ],
                        [
                            158.80687,
                            53.539473
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 176,
                "properties": {
                    "name": "Точка: 176 - Точка: 177",
                    "azimuth": "152 град 9 мин 2.4 с",
                    "pn": 0.0,
                    "distance": "12.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80687,
                            53.539473
                        ],
                        [
                            158.80672,
                            53.539388
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 177,
                "properties": {
                    "name": "Точка: 177 - Точка: 178",
                    "azimuth": "178 град 43 мин 5.2 с",
                    "pn": 0.0,
                    "distance": "18.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80672,
                            53.539388
                        ],
                        [
                            158.80647,
                            53.539382
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 178,
                "properties": {
                    "name": "Точка: 178 - Точка: 179",
                    "azimuth": "166 град 31 мин 48.9 с",
                    "pn": 0.0,
                    "distance": "44.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80647,
                            53.539382
                        ],
                        [
                            158.80589,
                            53.539233
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 179,
                "properties": {
                    "name": "Точка: 179 - Точка: 180",
                    "azimuth": "171 град 8 мин 46.0 с",
                    "pn": 0.0,
                    "distance": "61.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80589,
                            53.539233
                        ],
                        [
                            158.80507,
                            53.539096
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 180,
                "properties": {
                    "name": "Точка: 180 - Точка: 181",
                    "azimuth": "157 град 45 мин 13.8 с",
                    "pn": 0.0,
                    "distance": "24.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80507,
                            53.539096
                        ],
                        [
                            158.8047600000001,
                            53.53896
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 181,
                "properties": {
                    "name": "Точка: 181 - Точка: 182",
                    "azimuth": "171 град 24 мин 57.2 с",
                    "pn": 0.0,
                    "distance": "15.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8047600000001,
                            53.53896
                        ],
                        [
                            158.80455,
                            53.538926
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 182,
                "properties": {
                    "name": "Точка: 182 - Точка: 183",
                    "azimuth": "179 град 53 мин 15.1 с",
                    "pn": 0.0,
                    "distance": "70.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80455,
                            53.538926
                        ],
                        [
                            158.8036,
                            53.538924
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 183,
                "properties": {
                    "name": "Точка: 183 - Точка: 184",
                    "azimuth": "190 град 21 мин 58.9 с",
                    "pn": 0.0,
                    "distance": "59.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8036,
                            53.538924
                        ],
                        [
                            158.80281,
                            53.539079
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 184,
                "properties": {
                    "name": "Точка: 184 - Точка: 185",
                    "azimuth": "202 град 6 мин 31.1 с",
                    "pn": 0.0,
                    "distance": "22.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80281,
                            53.539079
                        ],
                        [
                            158.80253,
                            53.539201
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 185,
                "properties": {
                    "name": "Точка: 185 - Точка: 186",
                    "azimuth": "191 град 38 мин 2.9 с",
                    "pn": 0.0,
                    "distance": "18.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80253,
                            53.539201
                        ],
                        [
                            158.80229,
                            53.539254
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 186,
                "properties": {
                    "name": "Точка: 186 - Точка: 187",
                    "azimuth": "183 град 28 мин 4.8 с",
                    "pn": 0.0,
                    "distance": "14.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80229,
                            53.539254
                        ],
                        [
                            158.80209,
                            53.539267
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 187,
                "properties": {
                    "name": "Точка: 187 - Точка: 188",
                    "azimuth": "166 град 48 мин 52.6 с",
                    "pn": 0.0,
                    "distance": "29.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80209,
                            53.539267
                        ],
                        [
                            158.8017,
                            53.539169
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 188,
                "properties": {
                    "name": "Точка: 188 - Точка: 189",
                    "azimuth": "181 град 27 мин 23.6 с",
                    "pn": 0.0,
                    "distance": "57.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.8017,
                            53.539169
                        ],
                        [
                            158.80093,
                            53.53919
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 189,
                "properties": {
                    "name": "Точка: 189 - Точка: 190",
                    "azimuth": "191 град 6 мин 17.3 с",
                    "pn": 0.0,
                    "distance": "28.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80093,
                            53.53919
                        ],
                        [
                            158.80055,
                            53.53927
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 190,
                "properties": {
                    "name": "Точка: 190 - Точка: 191",
                    "azimuth": "184 град 45 мин 30.6 с",
                    "pn": 0.0,
                    "distance": "62.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.80055,
                            53.53927
                        ],
                        [
                            158.79971,
                            53.539345
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 191,
                "properties": {
                    "name": "Точка: 191 - Точка: 192",
                    "azimuth": "176 град 1 мин 1.2 с",
                    "pn": 0.0,
                    "distance": "58.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79971,
                            53.539345
                        ],
                        [
                            158.79892,
                            53.539286
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 192,
                "properties": {
                    "name": "Точка: 192 - Точка: 193",
                    "azimuth": "186 град 57 мин 54.2 с",
                    "pn": 0.0,
                    "distance": "21.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79892,
                            53.539286
                        ],
                        [
                            158.79863,
                            53.539324
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 193,
                "properties": {
                    "name": "Точка: 193 - Точка: 194",
                    "azimuth": "171 град 24 мин 45.9 с",
                    "pn": 0.0,
                    "distance": "53.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79863,
                            53.539324
                        ],
                        [
                            158.79792,
                            53.539209
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 194,
                "properties": {
                    "name": "Точка: 194 - Точка: 195",
                    "azimuth": "163 град 3 мин 42.0 с",
                    "pn": 0.0,
                    "distance": "23.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79792,
                            53.539209
                        ],
                        [
                            158.79762,
                            53.539111
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 195,
                "properties": {
                    "name": "Точка: 195 - Точка: 196",
                    "azimuth": "174 град 7 мин 21.2 с",
                    "pn": 0.0,
                    "distance": "35.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79762,
                            53.539111
                        ],
                        [
                            158.79714,
                            53.539058
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 196,
                "properties": {
                    "name": "Точка: 196 - Точка: 197",
                    "azimuth": "160 град 32 мин 51.4 с",
                    "pn": 0.0,
                    "distance": "107.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79714,
                            53.539058
                        ],
                        [
                            158.79577,
                            53.538539
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 197,
                "properties": {
                    "name": "Точка: 197 - Точка: 198",
                    "azimuth": "157 град 41 мин 45.9 с",
                    "pn": 0.0,
                    "distance": "32.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79577,
                            53.538539
                        ],
                        [
                            158.79537,
                            53.538363
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 198,
                "properties": {
                    "name": "Точка: 198 - Точка: 199",
                    "azimuth": "142 град 36 мин 10.0 с",
                    "pn": 0.0,
                    "distance": "14.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79537,
                            53.538363
                        ],
                        [
                            158.79522,
                            53.53824
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 199,
                "properties": {
                    "name": "Точка: 199 - Точка: 200",
                    "azimuth": "163 град 31 мин 55.5 с",
                    "pn": 0.0,
                    "distance": "31.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79522,
                            53.53824
                        ],
                        [
                            158.79481,
                            53.53811
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 200,
                "properties": {
                    "name": "Точка: 200 - Точка: 201",
                    "azimuth": "174 град 20 мин 34.7 с",
                    "pn": 0.0,
                    "distance": "11.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79481,
                            53.53811
                        ],
                        [
                            158.79465,
                            53.538093
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 201,
                "properties": {
                    "name": "Точка: 201 - Точка: 202",
                    "azimuth": "157 град 23 мин 31.4 с",
                    "pn": 0.0,
                    "distance": "12.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79465,
                            53.538093
                        ],
                        [
                            158.7945,
                            53.538026
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 202,
                "properties": {
                    "name": "Точка: 202 - Точка: 203",
                    "azimuth": "145 град 38 мин 25.6 с",
                    "pn": 0.0,
                    "distance": "16.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7945,
                            53.538026
                        ],
                        [
                            158.79432,
                            53.537894
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 203,
                "properties": {
                    "name": "Точка: 203 - Точка: 204",
                    "azimuth": "131 град 21 мин 24.1 с",
                    "pn": 0.0,
                    "distance": "30.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79432,
                            53.537894
                        ],
                        [
                            158.79405,
                            53.537565
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 204,
                "properties": {
                    "name": "Точка: 204 - Точка: 205",
                    "azimuth": "149 град 30 мин 17.6 с",
                    "pn": 0.0,
                    "distance": "35.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79405,
                            53.537565
                        ],
                        [
                            158.79364,
                            53.537306
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 205,
                "properties": {
                    "name": "Точка: 205 - Точка: 206",
                    "azimuth": "156 град 35 мин 11.3 с",
                    "pn": 0.0,
                    "distance": "61.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79364,
                            53.537306
                        ],
                        [
                            158.79288,
                            53.536953
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 206,
                "properties": {
                    "name": "Точка: 206 - Точка: 207",
                    "azimuth": "119 град 26 мин 48.6 с",
                    "pn": 0.0,
                    "distance": "16.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79288,
                            53.536953
                        ],
                        [
                            158.79277,
                            53.536744
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 207,
                "properties": {
                    "name": "Точка: 207 - Точка: 208",
                    "azimuth": "170 град 10 мин 38.5 с",
                    "pn": 0.0,
                    "distance": "15.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79277,
                            53.536744
                        ],
                        [
                            158.79256,
                            53.536705
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 208,
                "properties": {
                    "name": "Точка: 208 - Точка: 209",
                    "azimuth": "156 град 23 мин 40.3 с",
                    "pn": 0.0,
                    "distance": "38.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79256,
                            53.536705
                        ],
                        [
                            158.79208,
                            53.53648
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 209,
                "properties": {
                    "name": "Точка: 209 - Точка: 210",
                    "azimuth": "133 град 36 мин 7.4 с",
                    "pn": 0.0,
                    "distance": "61.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79208,
                            53.53648
                        ],
                        [
                            158.79151,
                            53.535838
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 210,
                "properties": {
                    "name": "Точка: 210 - Точка: 211",
                    "azimuth": "140 град 54 мин 33.9 с",
                    "pn": 0.0,
                    "distance": "26.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79151,
                            53.535838
                        ],
                        [
                            158.79123,
                            53.535594
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 211,
                "properties": {
                    "name": "Точка: 211 - Точка: 212",
                    "azimuth": "157 град 50 мин 28.5 с",
                    "pn": 0.0,
                    "distance": "30.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79123,
                            53.535594
                        ],
                        [
                            158.79085,
                            53.535428
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 212,
                "properties": {
                    "name": "Точка: 212 - Точка: 213",
                    "azimuth": "144 град 0 мин 11.1 с",
                    "pn": 0.0,
                    "distance": "48.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79085,
                            53.535428
                        ],
                        [
                            158.79032,
                            53.535015
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 213,
                "properties": {
                    "name": "Точка: 213 - Точка: 214",
                    "azimuth": "170 град 24 мин 33.1 с",
                    "pn": 0.0,
                    "distance": "12.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79032,
                            53.535015
                        ],
                        [
                            158.79016,
                            53.534986
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 214,
                "properties": {
                    "name": "Точка: 214 - Точка: 215",
                    "azimuth": "133 град 50 мин 54.7 с",
                    "pn": 0.0,
                    "distance": "12.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79016,
                            53.534986
                        ],
                        [
                            158.79004,
                            53.534852
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 215,
                "properties": {
                    "name": "Точка: 215 - Точка: 216",
                    "azimuth": "145 град 2 мин 20.4 с",
                    "pn": 0.0,
                    "distance": "27.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.79004,
                            53.534852
                        ],
                        [
                            158.78974,
                            53.534627
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 216,
                "properties": {
                    "name": "Точка: 216 - Точка: 217",
                    "azimuth": "152 град 34 мин 43.5 с",
                    "pn": 0.0,
                    "distance": "19.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78974,
                            53.534627
                        ],
                        [
                            158.78951,
                            53.534499
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 217,
                "properties": {
                    "name": "Точка: 217 - Точка: 218",
                    "azimuth": "142 град 37 мин 32.5 с",
                    "pn": 0.0,
                    "distance": "28.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78951,
                            53.534499
                        ],
                        [
                            158.7892,
                            53.534245
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 218,
                "properties": {
                    "name": "Точка: 218 - Точка: 219",
                    "azimuth": "170 град 44 мин 2.9 с",
                    "pn": 0.0,
                    "distance": "6.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7892,
                            53.534245
                        ],
                        [
                            158.78912,
                            53.534231
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 219,
                "properties": {
                    "name": "Точка: 219 - Точка: 220",
                    "azimuth": "136 град 25 мин 6.3 с",
                    "pn": 0.0,
                    "distance": "24.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78912,
                            53.534231
                        ],
                        [
                            158.78888,
                            53.533986
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 220,
                "properties": {
                    "name": "Точка: 220 - Точка: 221",
                    "azimuth": "122 град 26 мин 32.5 с",
                    "pn": 0.0,
                    "distance": "11.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78888,
                            53.533986
                        ],
                        [
                            158.7888,
                            53.533851
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 221,
                "properties": {
                    "name": "Точка: 221 - Точка: 222",
                    "azimuth": "156 град 6 мин 55.2 с",
                    "pn": 0.0,
                    "distance": "29.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7888,
                            53.533851
                        ],
                        [
                            158.78844,
                            53.53368
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 222,
                "properties": {
                    "name": "Точка: 222 - Точка: 223",
                    "azimuth": "109 град 22 мин 35.7 с",
                    "pn": 0.0,
                    "distance": "4.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78844,
                            53.53368
                        ],
                        [
                            158.78842,
                            53.533619
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 223,
                "properties": {
                    "name": "Точка: 223 - Точка: 224",
                    "azimuth": "152 град 22 мин 5.5 с",
                    "pn": 0.0,
                    "distance": "10.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78842,
                            53.533619
                        ],
                        [
                            158.78829,
                            53.533546
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 224,
                "properties": {
                    "name": "Точка: 224 - Точка: 225",
                    "azimuth": "135 град 5 мин 31.7 с",
                    "pn": 0.0,
                    "distance": "13.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78829,
                            53.533546
                        ],
                        [
                            158.78816,
                            53.533407
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 225,
                "properties": {
                    "name": "Точка: 225 - Точка: 226",
                    "azimuth": "106 град 35 мин 32.1 с",
                    "pn": 0.0,
                    "distance": "7.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78816,
                            53.533407
                        ],
                        [
                            158.78813,
                            53.533299
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 226,
                "properties": {
                    "name": "Точка: 226 - Точка: 227",
                    "azimuth": "135 град 33 мин 41.9 с",
                    "pn": 0.0,
                    "distance": "28.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78813,
                            53.533299
                        ],
                        [
                            158.78786,
                            53.533015
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 227,
                "properties": {
                    "name": "Точка: 227 - Точка: 228",
                    "azimuth": "154 град 20 мин 35.0 с",
                    "pn": 0.0,
                    "distance": "48.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78786,
                            53.533015
                        ],
                        [
                            158.78727,
                            53.532711
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 228,
                "properties": {
                    "name": "Точка: 228 - Точка: 229",
                    "azimuth": "129 град 10 мин 51.9 с",
                    "pn": 0.0,
                    "distance": "36.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78727,
                            53.532711
                        ],
                        [
                            158.78696,
                            53.532303
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 229,
                "properties": {
                    "name": "Точка: 229 - Точка: 230",
                    "azimuth": "145 град 56 мин 46.5 с",
                    "pn": 0.0,
                    "distance": "7.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78696,
                            53.532303
                        ],
                        [
                            158.78688,
                            53.532245
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 230,
                "properties": {
                    "name": "Точка: 230 - Точка: 231",
                    "azimuth": "169 град 26 мин 18.9 с",
                    "pn": 0.0,
                    "distance": "12.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78688,
                            53.532245
                        ],
                        [
                            158.78671,
                            53.532211
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 231,
                "properties": {
                    "name": "Точка: 231 - Точка: 232",
                    "azimuth": "145 град 16 мин 46.1 с",
                    "pn": 0.0,
                    "distance": "27.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78671,
                            53.532211
                        ],
                        [
                            158.78641,
                            53.531988
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 232,
                "properties": {
                    "name": "Точка: 232 - Точка: 233",
                    "azimuth": "130 град 24 мин 32.9 с",
                    "pn": 0.0,
                    "distance": "34.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78641,
                            53.531988
                        ],
                        [
                            158.78611,
                            53.53161
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 233,
                "properties": {
                    "name": "Точка: 233 - Точка: 234",
                    "azimuth": "99 град 30 мин 53.2 с",
                    "pn": 0.0,
                    "distance": "4.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78611,
                            53.53161
                        ],
                        [
                            158.7861,
                            53.531546
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 234,
                "properties": {
                    "name": "Точка: 234 - Точка: 235",
                    "azimuth": "125 град 26 мин 27.3 с",
                    "pn": 0.0,
                    "distance": "17.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7861,
                            53.531546
                        ],
                        [
                            158.78596,
                            53.531335
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 235,
                "properties": {
                    "name": "Точка: 235 - Точка: 236",
                    "azimuth": "103 град 33 мин 10.4 с",
                    "pn": 0.0,
                    "distance": "19.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78596,
                            53.531335
                        ],
                        [
                            158.7859,
                            53.531068
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 236,
                "properties": {
                    "name": "Точка: 236 - Точка: 237",
                    "azimuth": "133 град 42 мин 26.3 с",
                    "pn": 0.0,
                    "distance": "9.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7859,
                            53.531068
                        ],
                        [
                            158.78581,
                            53.530967
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 237,
                "properties": {
                    "name": "Точка: 237 - Точка: 238",
                    "azimuth": "167 град 25 мин 19.1 с",
                    "pn": 0.0,
                    "distance": "46.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78581,
                            53.530967
                        ],
                        [
                            158.7852,
                            53.530821
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 238,
                "properties": {
                    "name": "Точка: 238 - Точка: 239",
                    "azimuth": "146 град 18 мин 2.2 с",
                    "pn": 0.0,
                    "distance": "23.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7852,
                            53.530821
                        ],
                        [
                            158.78494,
                            53.530635
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 239,
                "properties": {
                    "name": "Точка: 239 - Точка: 240",
                    "azimuth": "169 град 17 мин 43.5 с",
                    "pn": 0.0,
                    "distance": "27.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78494,
                            53.530635
                        ],
                        [
                            158.78458,
                            53.530562
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 240,
                "properties": {
                    "name": "Точка: 240 - Точка: 241",
                    "azimuth": "155 град 10 мин 18.9 с",
                    "pn": 0.0,
                    "distance": "22.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78458,
                            53.530562
                        ],
                        [
                            158.78431,
                            53.530428
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 241,
                "properties": {
                    "name": "Точка: 241 - Точка: 242",
                    "azimuth": "120 град 6 мин 24.8 с",
                    "pn": 0.0,
                    "distance": "14.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78431,
                            53.530428
                        ],
                        [
                            158.78421,
                            53.530243
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 242,
                "properties": {
                    "name": "Точка: 242 - Точка: 243",
                    "azimuth": "140 град 0 мин 12.0 с",
                    "pn": 0.0,
                    "distance": "16.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78421,
                            53.530243
                        ],
                        [
                            158.78404,
                            53.53009
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 243,
                "properties": {
                    "name": "Точка: 243 - Точка: 244",
                    "azimuth": "157 град 42 мин 37.0 с",
                    "pn": 0.0,
                    "distance": "58.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78404,
                            53.53009
                        ],
                        [
                            158.78331,
                            53.529769
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 244,
                "properties": {
                    "name": "Точка: 244 - Точка: 245",
                    "azimuth": "109 град 33 мин 18.7 с",
                    "pn": 0.0,
                    "distance": "22.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78331,
                            53.529769
                        ],
                        [
                            158.78321,
                            53.529467
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 245,
                "properties": {
                    "name": "Точка: 245 - Точка: 246",
                    "azimuth": "127 град 54 мин 13.4 с",
                    "pn": 0.0,
                    "distance": "32.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78321,
                            53.529467
                        ],
                        [
                            158.78294,
                            53.529095
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 246,
                "properties": {
                    "name": "Точка: 246 - Точка: 247",
                    "azimuth": "113 град 58 мин 20.1 с",
                    "pn": 0.0,
                    "distance": "14.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78294,
                            53.529095
                        ],
                        [
                            158.78286,
                            53.528902
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 247,
                "properties": {
                    "name": "Точка: 247 - Точка: 248",
                    "azimuth": "143 град 53 мин 45.5 с",
                    "pn": 0.0,
                    "distance": "15.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78286,
                            53.528902
                        ],
                        [
                            158.78269,
                            53.528769
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 248,
                "properties": {
                    "name": "Точка: 248 - Точка: 249",
                    "azimuth": "130 град 1 мин 41.2 с",
                    "pn": 0.0,
                    "distance": "40.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78269,
                            53.528769
                        ],
                        [
                            158.78234,
                            53.528322
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 249,
                "properties": {
                    "name": "Точка: 249 - Точка: 250",
                    "azimuth": "120 град 47 мин 34.9 с",
                    "pn": 0.0,
                    "distance": "13.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78234,
                            53.528322
                        ],
                        [
                            158.78225,
                            53.52816
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 250,
                "properties": {
                    "name": "Точка: 250 - Точка: 251",
                    "azimuth": "66 град 54 мин 51.0 с",
                    "pn": 0.0,
                    "distance": "22.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78225,
                            53.52816
                        ],
                        [
                            158.78237,
                            53.527858
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 251,
                "properties": {
                    "name": "Точка: 251 - Точка: 252",
                    "azimuth": "115 град 37 мин 55.9 с",
                    "pn": 0.0,
                    "distance": "24.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78237,
                            53.527858
                        ],
                        [
                            158.78223,
                            53.527545
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 252,
                "properties": {
                    "name": "Точка: 252 - Точка: 253",
                    "azimuth": "99 град 33 мин 6.1 с",
                    "pn": 0.0,
                    "distance": "17.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78223,
                            53.527545
                        ],
                        [
                            158.78219,
                            53.52729
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 253,
                "properties": {
                    "name": "Точка: 253 - Точка: 254",
                    "azimuth": "141 град 52 мин 54.8 с",
                    "pn": 0.0,
                    "distance": "11.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78219,
                            53.52729
                        ],
                        [
                            158.78207,
                            53.527189
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 254,
                "properties": {
                    "name": "Точка: 254 - Точка: 255",
                    "azimuth": "125 град 30 мин 50.5 с",
                    "pn": 0.0,
                    "distance": "40.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78207,
                            53.527189
                        ],
                        [
                            158.7817500000001,
                            53.526708
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 255,
                "properties": {
                    "name": "Точка: 255 - Точка: 256",
                    "azimuth": "166 град 2 мин 23.6 с",
                    "pn": 0.0,
                    "distance": "13.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7817500000001,
                            53.526708
                        ],
                        [
                            158.7815700000001,
                            53.52666
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 256,
                "properties": {
                    "name": "Точка: 256 - Точка: 257",
                    "azimuth": "135 град 9 мин 44.1 с",
                    "pn": 0.0,
                    "distance": "25.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7815700000001,
                            53.52666
                        ],
                        [
                            158.78133,
                            53.526404
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 257,
                "properties": {
                    "name": "Точка: 257 - Точка: 258",
                    "azimuth": "188 град 23 мин 46.3 с",
                    "pn": 0.0,
                    "distance": "9.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78133,
                            53.526404
                        ],
                        [
                            158.7812100000001,
                            53.526423
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 258,
                "properties": {
                    "name": "Точка: 258 - Точка: 259",
                    "azimuth": "157 град 34 мин 3.1 с",
                    "pn": 0.0,
                    "distance": "5.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7812100000001,
                            53.526423
                        ],
                        [
                            158.78114,
                            53.526392
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 259,
                "properties": {
                    "name": "Точка: 259 - Точка: 260",
                    "azimuth": "128 град 38 мин 38.5 с",
                    "pn": 0.0,
                    "distance": "14.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78114,
                            53.526392
                        ],
                        [
                            158.78102,
                            53.526231
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 260,
                "properties": {
                    "name": "Точка: 260 - Точка: 261",
                    "azimuth": "162 град 13 мин 56.0 с",
                    "pn": 0.0,
                    "distance": "24.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78102,
                            53.526231
                        ],
                        [
                            158.7807,
                            53.526121
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 261,
                "properties": {
                    "name": "Точка: 261 - Точка: 262",
                    "azimuth": "148 град 16 мин 32.9 с",
                    "pn": 0.0,
                    "distance": "16.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7807,
                            53.526121
                        ],
                        [
                            158.78051,
                            53.525995
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 262,
                "properties": {
                    "name": "Точка: 262 - Точка: 263",
                    "azimuth": "167 град 41 мин 13.6 с",
                    "pn": 0.0,
                    "distance": "31.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78051,
                            53.525995
                        ],
                        [
                            158.7801,
                            53.525899
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 263,
                "properties": {
                    "name": "Точка: 263 - Точка: 264",
                    "azimuth": "111 град 40 мин 6.2 с",
                    "pn": 0.0,
                    "distance": "12.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7801,
                            53.525899
                        ],
                        [
                            158.78004,
                            53.525737
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 264,
                "properties": {
                    "name": "Точка: 264 - Точка: 265",
                    "azimuth": "130 град 38 мин 8.9 с",
                    "pn": 0.0,
                    "distance": "13.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.78004,
                            53.525737
                        ],
                        [
                            158.77992,
                            53.525587
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 265,
                "properties": {
                    "name": "Точка: 265 - Точка: 266",
                    "azimuth": "174 град 44 мин 45.2 с",
                    "pn": 0.0,
                    "distance": "55.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77992,
                            53.525587
                        ],
                        [
                            158.77918,
                            53.525514
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 266,
                "properties": {
                    "name": "Точка: 266 - Точка: 267",
                    "azimuth": "105 град 39 мин 59.2 с",
                    "pn": 0.0,
                    "distance": "11.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77918,
                            53.525514
                        ],
                        [
                            158.77914,
                            53.525361
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 267,
                "properties": {
                    "name": "Точка: 267 - Точка: 268",
                    "azimuth": "159 град 33 мин 2.6 с",
                    "pn": 0.0,
                    "distance": "21.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77914,
                            53.525361
                        ],
                        [
                            158.77887,
                            53.525253
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 268,
                "properties": {
                    "name": "Точка: 268 - Точка: 269",
                    "azimuth": "151 град 0 мин 27.5 с",
                    "pn": 0.0,
                    "distance": "15.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77887,
                            53.525253
                        ],
                        [
                            158.77869,
                            53.525146
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 269,
                "properties": {
                    "name": "Точка: 269 - Точка: 270",
                    "azimuth": "90 град 0 мин 0.0 с",
                    "pn": 0.0,
                    "distance": "3.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77869,
                            53.525146
                        ],
                        [
                            158.77869,
                            53.525097
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 270,
                "properties": {
                    "name": "Точка: 270 - Точка: 271",
                    "azimuth": "150 град 16 мин 30.4 с",
                    "pn": 0.0,
                    "distance": "6.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77869,
                            53.525097
                        ],
                        [
                            158.77861,
                            53.525048
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 271,
                "properties": {
                    "name": "Точка: 271 - Точка: 272",
                    "azimuth": "165 град 2 мин 51.4 с",
                    "pn": 0.0,
                    "distance": "28.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77861,
                            53.525048
                        ],
                        [
                            158.77824,
                            53.524942
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 272,
                "properties": {
                    "name": "Точка: 272 - Точка: 273",
                    "azimuth": "180 град 53 мин 24.4 с",
                    "pn": 0.0,
                    "distance": "26.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77824,
                            53.524942
                        ],
                        [
                            158.77788,
                            53.524948
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 273,
                "properties": {
                    "name": "Точка: 273 - Точка: 274",
                    "azimuth": "152 град 47 мин 43.5 с",
                    "pn": 0.0,
                    "distance": "29.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77788,
                            53.524948
                        ],
                        [
                            158.77753,
                            53.524755
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 274,
                "properties": {
                    "name": "Точка: 274 - Точка: 275",
                    "azimuth": "142 град 3 мин 30.6 с",
                    "pn": 0.0,
                    "distance": "10.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77753,
                            53.524755
                        ],
                        [
                            158.77742,
                            53.524663
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 275,
                "properties": {
                    "name": "Точка: 275 - Точка: 276",
                    "azimuth": "119 град 1 мин 28.9 с",
                    "pn": 0.0,
                    "distance": "9.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77742,
                            53.524663
                        ],
                        [
                            158.77736,
                            53.524547
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 276,
                "properties": {
                    "name": "Точка: 276 - Точка: 277",
                    "azimuth": "111 град 4 мин 39.8 с",
                    "pn": 0.0,
                    "distance": "12.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77736,
                            53.524547
                        ],
                        [
                            158.7773,
                            53.52438
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 277,
                "properties": {
                    "name": "Точка: 277 - Точка: 278",
                    "azimuth": "41 град 31 мин 37.9 с",
                    "pn": 0.0,
                    "distance": "4.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7773,
                            53.52438
                        ],
                        [
                            158.77734,
                            53.524342
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 278,
                "properties": {
                    "name": "Точка: 278 - Точка: 279",
                    "azimuth": "118 град 43 мин 41.5 с",
                    "pn": 0.0,
                    "distance": "21.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77734,
                            53.524342
                        ],
                        [
                            158.7772,
                            53.524068
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 279,
                "properties": {
                    "name": "Точка: 279 - Точка: 280",
                    "azimuth": "145 град 4 мин 11.6 с",
                    "pn": 0.0,
                    "distance": "57.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7772,
                            53.524068
                        ],
                        [
                            158.77657,
                            53.523596
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 280,
                "properties": {
                    "name": "Точка: 280 - Точка: 281",
                    "azimuth": "155 град 6 мин 0.1 с",
                    "pn": 0.0,
                    "distance": "40.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77657,
                            53.523596
                        ],
                        [
                            158.77608,
                            53.523352
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 281,
                "properties": {
                    "name": "Точка: 281 - Точка: 282",
                    "azimuth": "141 град 57 мин 29.9 с",
                    "pn": 0.0,
                    "distance": "31.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77608,
                            53.523352
                        ],
                        [
                            158.77575,
                            53.523075
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 282,
                "properties": {
                    "name": "Точка: 282 - Точка: 283",
                    "azimuth": "179 град 14 мин 13.4 с",
                    "pn": 0.0,
                    "distance": "41.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77575,
                            53.523075
                        ],
                        [
                            158.77519,
                            53.523067
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 283,
                "properties": {
                    "name": "Точка: 283 - Точка: 284",
                    "azimuth": "147 град 42 мин 18.2 с",
                    "pn": 0.0,
                    "distance": "71.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77519,
                            53.523067
                        ],
                        [
                            158.77437,
                            53.522511
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 284,
                "properties": {
                    "name": "Точка: 284 - Точка: 285",
                    "azimuth": "184 град 2 мин 31.2 с",
                    "pn": 0.0,
                    "distance": "46.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77437,
                            53.522511
                        ],
                        [
                            158.77375,
                            53.522558
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 285,
                "properties": {
                    "name": "Точка: 285 - Точка: 286",
                    "azimuth": "197 град 3 мин 14.8 с",
                    "pn": 0.0,
                    "distance": "42.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77375,
                            53.522558
                        ],
                        [
                            158.7732,
                            53.522739
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 286,
                "properties": {
                    "name": "Точка: 286 - Точка: 287",
                    "azimuth": "171 град 54 мин 0.4 с",
                    "pn": 0.0,
                    "distance": "83.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7732,
                            53.522739
                        ],
                        [
                            158.77208,
                            53.522568
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 287,
                "properties": {
                    "name": "Точка: 287 - Точка: 288",
                    "azimuth": "185 град 5 мин 4.7 с",
                    "pn": 0.0,
                    "distance": "49.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77208,
                            53.522568
                        ],
                        [
                            158.77142,
                            53.522631
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 288,
                "properties": {
                    "name": "Точка: 288 - Точка: 289",
                    "azimuth": "168 град 45 мин 11.2 с",
                    "pn": 0.0,
                    "distance": "79.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77142,
                            53.522631
                        ],
                        [
                            158.77037,
                            53.522407
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 289,
                "properties": {
                    "name": "Точка: 289 - Точка: 290",
                    "azimuth": "156 град 36 мин 39.8 с",
                    "pn": 0.0,
                    "distance": "40.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.77037,
                            53.522407
                        ],
                        [
                            158.76987,
                            53.522175
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 290,
                "properties": {
                    "name": "Точка: 290 - Точка: 291",
                    "azimuth": "144 град 10 мин 50.4 с",
                    "pn": 0.0,
                    "distance": "32.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76987,
                            53.522175
                        ],
                        [
                            158.76952,
                            53.521904
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 291,
                "properties": {
                    "name": "Точка: 291 - Точка: 292",
                    "azimuth": "137 град 53 мин 24.5 с",
                    "pn": 0.0,
                    "distance": "33.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76952,
                            53.521904
                        ],
                        [
                            158.76919,
                            53.521584
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 292,
                "properties": {
                    "name": "Точка: 292 - Точка: 293",
                    "azimuth": "125 град 25 мин 21.7 с",
                    "pn": 0.0,
                    "distance": "30.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76919,
                            53.521584
                        ],
                        [
                            158.76895,
                            53.521222
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 293,
                "properties": {
                    "name": "Точка: 293 - Точка: 294",
                    "azimuth": "133 град 10 мин 39.1 с",
                    "pn": 0.0,
                    "distance": "32.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76895,
                            53.521222
                        ],
                        [
                            158.76865,
                            53.520879
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 294,
                "properties": {
                    "name": "Точка: 294 - Точка: 295",
                    "azimuth": "101 град 21 мин 13.6 с",
                    "pn": 0.0,
                    "distance": "26.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76865,
                            53.520879
                        ],
                        [
                            158.76858,
                            53.520505
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 295,
                "properties": {
                    "name": "Точка: 295 - Точка: 296",
                    "azimuth": "126 град 23 мин 31.6 с",
                    "pn": 0.0,
                    "distance": "11.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76858,
                            53.520505
                        ],
                        [
                            158.76849,
                            53.520374
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 296,
                "properties": {
                    "name": "Точка: 296 - Точка: 297",
                    "azimuth": "99 град 20 мин 38.2 с",
                    "pn": 0.0,
                    "distance": "22.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76849,
                            53.520374
                        ],
                        [
                            158.76844,
                            53.520048
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 297,
                "properties": {
                    "name": "Точка: 297 - Точка: 298",
                    "azimuth": "107 град 57 мин 54.1 с",
                    "pn": 0.0,
                    "distance": "55.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76844,
                            53.520048
                        ],
                        [
                            158.76821,
                            53.519287
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 298,
                "properties": {
                    "name": "Точка: 298 - Точка: 299",
                    "azimuth": "117 град 22 мин 16.8 с",
                    "pn": 0.0,
                    "distance": "29.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76821,
                            53.519287
                        ],
                        [
                            158.76803,
                            53.518914
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 299,
                "properties": {
                    "name": "Точка: 299 - Точка: 300",
                    "azimuth": "100 град 49 мин 1.1 с",
                    "pn": 0.0,
                    "distance": "79.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76803,
                            53.518914
                        ],
                        [
                            158.76783,
                            53.517791
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 300,
                "properties": {
                    "name": "Точка: 300 - Точка: 301",
                    "azimuth": "139 град 0 мин 53.7 с",
                    "pn": 0.0,
                    "distance": "107.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76783,
                            53.517791
                        ],
                        [
                            158.76674,
                            53.516775
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 301,
                "properties": {
                    "name": "Точка: 301 - Точка: 302",
                    "azimuth": "131 град 8 мин 42.0 с",
                    "pn": 0.0,
                    "distance": "68.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76674,
                            53.516775
                        ],
                        [
                            158.76613,
                            53.516026
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 302,
                "properties": {
                    "name": "Точка: 302 - Точка: 303",
                    "azimuth": "123 град 19 мин 12.0 с",
                    "pn": 0.0,
                    "distance": "33.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76613,
                            53.516026
                        ],
                        [
                            158.76588,
                            53.515618
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 303,
                "properties": {
                    "name": "Точка: 303 - Точка: 304",
                    "azimuth": "100 град 41 мин 8.1 с",
                    "pn": 0.0,
                    "distance": "28.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76588,
                            53.515618
                        ],
                        [
                            158.7658100000001,
                            53.51522
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 304,
                "properties": {
                    "name": "Точка: 304 - Точка: 305",
                    "azimuth": "130 град 27 мин 53.8 с",
                    "pn": 0.0,
                    "distance": "29.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7658100000001,
                            53.51522
                        ],
                        [
                            158.76555,
                            53.514893
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 305,
                "properties": {
                    "name": "Точка: 305 - Точка: 306",
                    "azimuth": "135 град 47 мин 14.9 с",
                    "pn": 0.0,
                    "distance": "33.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76555,
                            53.514893
                        ],
                        [
                            158.76523,
                            53.514559
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 306,
                "properties": {
                    "name": "Точка: 306 - Точка: 307",
                    "azimuth": "152 град 23 мин 44.0 с",
                    "pn": 0.0,
                    "distance": "34.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76523,
                            53.514559
                        ],
                        [
                            158.7648200000001,
                            53.514329
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 307,
                "properties": {
                    "name": "Точка: 307 - Точка: 308",
                    "azimuth": "145 град 17 мин 0.4 с",
                    "pn": 0.0,
                    "distance": "27.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7648200000001,
                            53.514329
                        ],
                        [
                            158.76452,
                            53.514106
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 308,
                "properties": {
                    "name": "Точка: 308 - Точка: 309",
                    "azimuth": "116 град 34 мин 4.3 с",
                    "pn": 0.0,
                    "distance": "91.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76452,
                            53.514106
                        ],
                        [
                            158.76397,
                            53.512926
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 309,
                "properties": {
                    "name": "Точка: 309 - Точка: 310",
                    "azimuth": "104 град 14 мин 38.3 с",
                    "pn": 0.0,
                    "distance": "114.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76397,
                            53.512926
                        ],
                        [
                            158.76359,
                            53.51132
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 310,
                "properties": {
                    "name": "Точка: 310 - Точка: 311",
                    "azimuth": "125 град 51 мин 54.1 с",
                    "pn": 0.0,
                    "distance": "31.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76359,
                            53.51132
                        ],
                        [
                            158.76334,
                            53.510949
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 311,
                "properties": {
                    "name": "Точка: 311 - Точка: 312",
                    "azimuth": "132 град 20 мин 22.7 с",
                    "pn": 0.0,
                    "distance": "34.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76334,
                            53.510949
                        ],
                        [
                            158.76303,
                            53.510584
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 312,
                "properties": {
                    "name": "Точка: 312 - Точка: 313",
                    "azimuth": "146 град 41 мин 41.2 с",
                    "pn": 0.0,
                    "distance": "36.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76303,
                            53.510584
                        ],
                        [
                            158.76262,
                            53.510295
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 313,
                "properties": {
                    "name": "Точка: 313 - Точка: 314",
                    "azimuth": "156 град 25 мин 43.0 с",
                    "pn": 0.0,
                    "distance": "38.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76262,
                            53.510295
                        ],
                        [
                            158.76215,
                            53.510075
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 314,
                "properties": {
                    "name": "Точка: 314 - Точка: 315",
                    "azimuth": "162 град 7 мин 4.9 с",
                    "pn": 0.0,
                    "distance": "40.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76215,
                            53.510075
                        ],
                        [
                            158.76163,
                            53.509895
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 315,
                "properties": {
                    "name": "Точка: 315 - Точка: 316",
                    "azimuth": "171 град 3 мин 40.6 с",
                    "pn": 0.0,
                    "distance": "24.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76163,
                            53.509895
                        ],
                        [
                            158.76131,
                            53.509841
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 316,
                "properties": {
                    "name": "Точка: 316 - Точка: 317",
                    "azimuth": "182 град 40 мин 5.8 с",
                    "pn": 0.0,
                    "distance": "20.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76131,
                            53.509841
                        ],
                        [
                            158.76103,
                            53.509855
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 317,
                "properties": {
                    "name": "Точка: 317 - Точка: 318",
                    "azimuth": "206 град 6 мин 18.3 с",
                    "pn": 0.0,
                    "distance": "28.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76103,
                            53.509855
                        ],
                        [
                            158.76068,
                            53.510039
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 318,
                "properties": {
                    "name": "Точка: 318 - Точка: 319",
                    "azimuth": "173 град 28 мин 27.3 с",
                    "pn": 0.0,
                    "distance": "32.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76068,
                            53.510039
                        ],
                        [
                            158.76024,
                            53.509985
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 319,
                "properties": {
                    "name": "Точка: 319 - Точка: 320",
                    "azimuth": "143 град 9 мин 28.6 с",
                    "pn": 0.0,
                    "distance": "24.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.76024,
                            53.509985
                        ],
                        [
                            158.75998,
                            53.509776
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 320,
                "properties": {
                    "name": "Точка: 320 - Точка: 321",
                    "azimuth": "194 град 7 мин 32.4 с",
                    "pn": 0.0,
                    "distance": "7.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75998,
                            53.509776
                        ],
                        [
                            158.75988,
                            53.509803
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 321,
                "properties": {
                    "name": "Точка: 321 - Точка: 322",
                    "azimuth": "125 град 38 мин 39.5 с",
                    "pn": 0.0,
                    "distance": "99.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75988,
                            53.509803
                        ],
                        [
                            158.7591000000001,
                            53.508636
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 322,
                "properties": {
                    "name": "Точка: 322 - Точка: 323",
                    "azimuth": "170 град 44 мин 9.6 с",
                    "pn": 0.0,
                    "distance": "6.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7591000000001,
                            53.508636
                        ],
                        [
                            158.75902,
                            53.508622
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 323,
                "properties": {
                    "name": "Точка: 323 - Точка: 324",
                    "azimuth": "82 град 15 мин 57.9 с",
                    "pn": 0.0,
                    "distance": "11.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75902,
                            53.508622
                        ],
                        [
                            158.75904,
                            53.508464
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 324,
                "properties": {
                    "name": "Точка: 324 - Точка: 325",
                    "azimuth": "100 град 12 мин 17.4 с",
                    "pn": 0.0,
                    "distance": "20.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75904,
                            53.508464
                        ],
                        [
                            158.75899,
                            53.508166
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 325,
                "properties": {
                    "name": "Точка: 325 - Точка: 326",
                    "azimuth": "135 град 14 мин 53.2 с",
                    "pn": 0.0,
                    "distance": "11.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75899,
                            53.508166
                        ],
                        [
                            158.75888,
                            53.508049
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 326,
                "properties": {
                    "name": "Точка: 326 - Точка: 327",
                    "azimuth": "150 град 20 мин 4.2 с",
                    "pn": 0.0,
                    "distance": "46.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75888,
                            53.508049
                        ],
                        [
                            158.75834,
                            53.507719
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 327,
                "properties": {
                    "name": "Точка: 327 - Точка: 328",
                    "azimuth": "141 град 44 мин 18.2 с",
                    "pn": 0.0,
                    "distance": "24.5 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75834,
                            53.507719
                        ],
                        [
                            158.75808,
                            53.507499
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 328,
                "properties": {
                    "name": "Точка: 328 - Точка: 329",
                    "azimuth": "137 град 0 мин 50.6 с",
                    "pn": 0.0,
                    "distance": "30.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75808,
                            53.507499
                        ],
                        [
                            158.75778,
                            53.507199
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 329,
                "properties": {
                    "name": "Точка: 329 - Точка: 330",
                    "azimuth": "115 град 44 мин 36.3 с",
                    "pn": 0.0,
                    "distance": "13.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75778,
                            53.507199
                        ],
                        [
                            158.7577,
                            53.507021
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 330,
                "properties": {
                    "name": "Точка: 330 - Точка: 331",
                    "azimuth": "142 град 33 мин 42.3 с",
                    "pn": 0.0,
                    "distance": "26.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7577,
                            53.507021
                        ],
                        [
                            158.75742,
                            53.506791
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 331,
                "properties": {
                    "name": "Точка: 331 - Точка: 332",
                    "azimuth": "117 град 11 мин 9.9 с",
                    "pn": 0.0,
                    "distance": "29.2 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75742,
                            53.506791
                        ],
                        [
                            158.75724,
                            53.506415
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 332,
                "properties": {
                    "name": "Точка: 332 - Точка: 333",
                    "azimuth": "26 град 25 мин 54.4 с",
                    "pn": 0.0,
                    "distance": "5.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75724,
                            53.506415
                        ],
                        [
                            158.7573000000001,
                            53.506383
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 333,
                "properties": {
                    "name": "Точка: 333 - Точка: 334",
                    "azimuth": "173 град 21 мин 16.6 с",
                    "pn": 0.0,
                    "distance": "6.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7573000000001,
                            53.506383
                        ],
                        [
                            158.75722,
                            53.506373
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 334,
                "properties": {
                    "name": "Точка: 334 - Точка: 335",
                    "azimuth": "110 град 57 мин 56.8 с",
                    "pn": 0.0,
                    "distance": "4.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75722,
                            53.506373
                        ],
                        [
                            158.7572,
                            53.506317
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 335,
                "properties": {
                    "name": "Точка: 335 - Точка: 336",
                    "azimuth": "99 град 26 мин 39.1 с",
                    "pn": 0.0,
                    "distance": "9.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7572,
                            53.506317
                        ],
                        [
                            158.75718,
                            53.506188
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 336,
                "properties": {
                    "name": "Точка: 336 - Точка: 337",
                    "azimuth": "79 град 3 мин 31.9 с",
                    "pn": 0.0,
                    "distance": "15.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75718,
                            53.506188
                        ],
                        [
                            158.75722,
                            53.505966
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 337,
                "properties": {
                    "name": "Точка: 337 - Точка: 338",
                    "azimuth": "107 град 38 мин 7.0 с",
                    "pn": 0.0,
                    "distance": "9.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75722,
                            53.505966
                        ],
                        [
                            158.75718,
                            53.505831
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 338,
                "properties": {
                    "name": "Точка: 338 - Точка: 339",
                    "azimuth": "118 град 45 мин 3.8 с",
                    "pn": 0.0,
                    "distance": "13.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75718,
                            53.505831
                        ],
                        [
                            158.75709,
                            53.505655
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 339,
                "properties": {
                    "name": "Точка: 339 - Точка: 340",
                    "azimuth": "138 град 44 мин 31.1 с",
                    "pn": 0.0,
                    "distance": "16.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75709,
                            53.505655
                        ],
                        [
                            158.75692,
                            53.505495
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 340,
                "properties": {
                    "name": "Точка: 340 - Точка: 341",
                    "azimuth": "149 град 6 мин 2.0 с",
                    "pn": 0.0,
                    "distance": "16.4 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75692,
                            53.505495
                        ],
                        [
                            158.75673,
                            53.505373
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 341,
                "properties": {
                    "name": "Точка: 341 - Точка: 342",
                    "azimuth": "171 град 54 мин 12.4 с",
                    "pn": 0.0,
                    "distance": "42.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75673,
                            53.505373
                        ],
                        [
                            158.75616,
                            53.505286
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 342,
                "properties": {
                    "name": "Точка: 342 - Точка: 343",
                    "azimuth": "163 град 40 мин 23.6 с",
                    "pn": 0.0,
                    "distance": "37.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75616,
                            53.505286
                        ],
                        [
                            158.75567,
                            53.505132
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 343,
                "properties": {
                    "name": "Точка: 343 - Точка: 344",
                    "azimuth": "158 град 42 мин 21.6 с",
                    "pn": 0.0,
                    "distance": "26.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75567,
                            53.505132
                        ],
                        [
                            158.75534,
                            53.504994
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 344,
                "properties": {
                    "name": "Точка: 344 - Точка: 345",
                    "azimuth": "148 град 16 мин 13.2 с",
                    "pn": 0.0,
                    "distance": "35.7 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75534,
                            53.504994
                        ],
                        [
                            158.75493,
                            53.504722
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 345,
                "properties": {
                    "name": "Точка: 345 - Точка: 346",
                    "azimuth": "178 град 33 мин 45.2 с",
                    "pn": 0.0,
                    "distance": "19.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75493,
                            53.504722
                        ],
                        [
                            158.75467,
                            53.504715
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 346,
                "properties": {
                    "name": "Точка: 346 - Точка: 347",
                    "azimuth": "154 град 23 мин 24.2 с",
                    "pn": 0.0,
                    "distance": "5.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75467,
                            53.504715
                        ],
                        [
                            158.7546,
                            53.504679
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 347,
                "properties": {
                    "name": "Точка: 347 - Точка: 348",
                    "azimuth": "172 град 43 мин 32.4 с",
                    "pn": 0.0,
                    "distance": "68.8 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7546,
                            53.504679
                        ],
                        [
                            158.75368,
                            53.504553
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 348,
                "properties": {
                    "name": "Точка: 348 - Точка: 349",
                    "azimuth": "158 град 46 мин 35.6 с",
                    "pn": 0.0,
                    "distance": "23.9 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75368,
                            53.504553
                        ],
                        [
                            158.75338,
                            53.504428
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 349,
                "properties": {
                    "name": "Точка: 349 - Точка: 350",
                    "azimuth": "169 град 34 мин 36.5 с",
                    "pn": 0.0,
                    "distance": "28.6 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75338,
                            53.504428
                        ],
                        [
                            158.753,
                            53.504353
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 350,
                "properties": {
                    "name": "Точка: 350 - Точка: 351",
                    "azimuth": "163 град 3 мин 43.2 с",
                    "pn": 0.0,
                    "distance": "55.0 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.753,
                            53.504353
                        ],
                        [
                            158.75229,
                            53.504121
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 351,
                "properties": {
                    "name": "Точка: 351 - Точка: 352",
                    "azimuth": "160 град 46 мин 34.4 с",
                    "pn": 0.0,
                    "distance": "91.1 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.75229,
                            53.504121
                        ],
                        [
                            158.7511300000001,
                            53.503687
                        ]
                    ]
                }
            },
            {
                "type": "Feature",
                "id": 352,
                "properties": {
                    "name": "Точка: 352 - Точка: 353",
                    "azimuth": "171 град 7 мин 24.9 с",
                    "pn": 0.0,
                    "distance": "83.3 п.ш."
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            158.7511300000001,
                            53.503687
                        ],
                        [
                            158.75002,
                            53.503501
                        ]
                    ]
                }
            }
        ]
    }
}
```
</details>

#### АПИ получения сотрудников и закрепленных за ними задач
```py
import requests
url = "https://swan-decent-shrew.ngrok-free.app/api/task/"
response = requests.post(url)
response.json()
```
#### Запрос на JS
```js
fetch('https://swan-decent-shrew.ngrok-free.app/api/task/')
    .then(response => response.json())
    .then(data => {
        const dataBlockContainer = document.getElementById('data-block-container');

        // Итерация по данным и создание блоков для каждого человека
        data.forEach(person => {
            const personBlock = document.createElement('div');
            personBlock.classList.add('person-block');
            personBlock.innerHTML = `
                <h2>${person.person_name}</h2>
            `;

            // Итерация по инцидентам каждого человека
            person.incidents.forEach(incident => {
                const personLatitude = incident.location.latitude;
                const personLongitude = incident.location.longitude;
                // Создание маркера и добавление его на карту
                const marker = L.marker([personLatitude, personLongitude]).addTo(map);
                markers.push(marker);

                // Создаем всплывающее окно с информацией об инциденте
                const popup = L.popup()
                    .setLatLng([personLatitude, personLongitude])
                    .setContent(`
                        <h3>Описание инцидента: ${incident.name}</h3>
                        <p>Координаты: ${personLatitude} широты, ${personLongitude} долготы</p>
                    `);
                marker.bindPopup(popup);

                const incidentBlock = document.createElement('div');
                incidentBlock.classList.add('incident-block');
                incidentBlock.innerHTML = `
                    <h2>Описание инцидента: ${incident.name}</h2>
                    <p>Фотография инцидента: ${incident.details}</p>
                    <p>Координаты: ${personLatitude} широты, ${personLongitude} долготы</p>
                    <button class="button" onclick="centerMapOnMarker(${personLatitude}, ${personLongitude})">Просмотреть на карте</button>
                `;
                dataBlockContainer.appendChild(personBlock);
                personBlock.appendChild(incidentBlock);
            });
        });
    })
    .catch(error => console.error('Ошибка при получении данных:', error));

```
#### Ответ:

<details>
[{"person_name": "\u0421\u0438\u0434\u043e\u0440\u043e\u0432 \u0421\u0438\u0434\u0440 \u0421\u0438\u0434\u043e\u0440\u043e\u0432\u0438\u0447", "incidents": [{"name": "\u041e\u0431\u043d\u0430\u0440\u0443\u0436\u0435\u043d\u0430 \u043c\u0443\u0441\u043e\u0440\u043d\u0430\u044f \u044f\u043c\u0430!", "location": {"latitude": 53.52663571089894, "longitude": 158.74797821044925}}]}, {"person_name": "\u041f\u0435\u0442\u0440\u043e\u0432 \u041f\u0435\u0442\u0440 \u041f\u0435\u0442\u0440\u043e\u0432\u0438\u0447", "incidents": []}, {"person_name": "\u0418\u0432\u0430\u043d\u043e\u0432 \u0418\u0432\u0430\u043d \u0418\u0432\u0430\u043d\u043e\u0432\u0438\u0447", "incidents": [{"name": "\u041f\u043e\u0436\u0430\u0440!", "location": {"latitude": 53.54193953598892, "longitude": 158.83209228515628}}]}]
</details>
