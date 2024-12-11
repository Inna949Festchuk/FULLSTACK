from flask import Flask, jsonify, request
from flask.views import MethodView # Материнский класс для создания CDUD
from models import Session, User
# Обработка ошибок:
# sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) 
# ОШИБКА:  повторяющееся значение ключа нарушает ограничение уникальности "app_users_name_key"
# DETAIL:  Ключ "(name)=(user_23)" уже существует.
# Обрабатываем эту ошибку:
from sqlalchemy.exc import IntegrityError

app = Flask("my_server") # Создаем приложение


# def hello_world(some_id):
#     json_data = request.json  # Обрабатываем входящий json из запроса
#     qs = request.args # Обрабатываем входящий query string из запроса
#     headers = request.headers # Обрабатываем входящие заголовки из запроса
#     # Смотрим что нам пришло от клиента
#     print(f'{some_id=}')
#     print(f'{json_data=}')
#     print(f'{qs=}')
#     print(f'{headers=}')

#     # Сериализуем объект словарь python (словарь, список, строку ...) 
#     # с помощью функции jsonify() и отправляем ответ клиенту
#     # в виде строки байтов - b`{JSON}
#     response = jsonify({"Hello": "world"})
#     return response

# # Привязываем функцию к url (забиндить)
# app.add_url_rule(
#     "/hello/world/<int:some_id>", 
#     view_func=hello_world, 
#     methods=["POST"])

# app.run()

# - - - - - - - - - - 
# ОБРАБОТКА ОШИБОК
# - - - - - - - - - - 

# Создаем класс ошибок, которые будут обрабатываться error_handler(error)
class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

@app.errorhandler(HttpError) # регистрируем функцию и передаем экземпляры класса ошибок
def error_handler(error: HttpError):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response 

def add_user(session, user):
    # Добавляем в сессию юзера
    session.add(user)
    # Обрабатываем ошибку IntegrityError
    try:
        # Коминтим изменения
        session.commit()
    except IntegrityError as er:
        # response = jsonify({'error': "user alredy exist"})
        # response.status_code = 409
        raise HttpError(400, "user alredy exist") # созданный выше класс ошибок
        # return response
        
# ЭТУ ФУНКЦИЮ МОЖНО ДОРАБОТАТЬ ВСТРОЕННЫМ ВО FLASK ОБРАБОТЧИКОМ ОШИБОК ERR-HANDLER
# который позволяет зарегистрировать функцию, которая будет обрабатывать
# те ошибки, которые мы скажем ей и возвращать нужный нам ответ клиенту

# - - - - - - - - - - 
# - - - - - - - - - - 

# Создаем класс, который реализует логику CRUD 
# для пользователей наследуясьот материнского
# класса MethodView
class UserView(MethodView):
    def get(self, user_id: int):
        pass 

    def post(self):
        # Десериализуем строку байтов - b`{JSON}, 
        # прешедший в запросе от клиента в объект {JSON} (упорядоченный словарь)
        json_data = request.json
        # Открываем сессию
        with Session() as session:
            # Поля, JSON-а ("id", "name", "password" и "registration_time"),
            # распоковав его, присваиваем классу User(), сформировав экземпляр класса
            # user - его еще называют объектом user модели Юзер
            # user = User(**json_data)
            # либо так, что одно и тоже
            user = User(
                name=json_data['name'],
                password=json_data['password']
            )
            # ПЕРЕМЕЩАЕМ ЭТОТ КОД В ОТДЕЛЬНУЮ ФУНКЦИЮ add_user()
            # - - - - - - - - - - 
            # # Добавляем в сессию юзера
            # session.add(user)
            # # Обрабатываем ошибку IntegrityError
            # try:
            #     # Коминтим изменения
            #     session.commit()
            # except IntegrityError:
            #     response = jsonify({'error': "user alredy exist"})
            #     response.status_code = 409
            #     return response

            # - - - - - - - - - - 
            # ВЫЗЫВАЕМ ОБРАБОТЧИК ОШИБОК
            # - - - - - - - - - - 
            add_user(session, user)
            # - - - - - - - - - -

            # C помощью свойства класса User() - dict, определенного в файле models.py, 
            # преобразуем объект user модели в объект словарь python: user.dict.
            # Сериализуем объект словарь python в байтовую строку - b`{JSON} с помощью функции jsonify()
            # и отправляем ответ клиенту
            return jsonify(user.dict)

    def path(self, user_id: int):
        pass 

    def delite(self, user_id: int):
        pass 

# Преобразовываем класс UserView в представление(вьюшку) 
# для привязки к нему url-ов
user_view = UserView.as_view("user")

# Выполняем роутинг для вьюшки
app.add_url_rule(
    "/user/<int:user_id>", # для "GET", "PATH", "DELETE"
    view_func=user_view,
    methods=["GET", "PATH", "DELETE"] 
)
app.add_url_rule(
    "/user", # для "POST"
    view_func=user_view,
    methods=["POST"] 
)

app.run()