from flask import Flask, jsonify, request
from flask.views import MethodView # Материнский класс для создания CDUD
from models import Session, User

# Обработка ошибок:
# sqlalchemy.exc.IntegrityError: (psycopg2.errors.UniqueViolation) 
# ОШИБКА:  повторяющееся значение ключа нарушает ограничение уникальности "app_users_name_key"
# DETAIL:  Ключ "(name)=(user_23)" уже существует.
# Обрабатываем эту ошибку:
from sqlalchemy.exc import IntegrityError

from shema import CreatUser, UpdateUser # импортируем схемы валидации созданные в  schema.py
from pydantic import ValidationError

from flask_bcrypt import Bcrypt # Для flask нужна эта библиотека

app = Flask("my_server") # Создаем приложение

# - - - - - - - - - - 
# ХЕШИРОВАНИЕ ПАРОЛЕЙ
# - - - - - - - - - - 
bcrypt = Bcrypt(app)

def hash_password(password: str) -> str:
    '''
    '''
    
    password_bytes = password.encode() # преобразовываем пароль в байты
    password_hashed_bytes = bcrypt.generate_password_hash(password_bytes) # получаю захешированный пароль в виде байтов
    password_hashed = password_hashed_bytes.decode() # преобразуем байты в строчку
    return password_hashed

# - - - - - - - - - - 
# ПРОВЕРКА ПАРОЛЕЙ (применять не будем просто напишем)
# будет проверять пароль клиента с тем что хранится в БД,
# если все правильно, будем говорить что пользователь залогинен
# - - - - - - - - - - 
def check_password(password: str, hashed_password: str) -> bool:    
    password = password.encode()
    hashed_password = hash_password.encode()
    return bcrypt.check_password_hash(hashed_password, password)

# - - - - - - - - - - 
# ОБРАБОТКА ОШИБОК
# - - - - - - - - - - 
# Создаем класс ошибок, которые будут обрабатываться error_handler(error)
class HttpError(Exception):

    def __init__(self, status_code, message):
        self.status_code = status_code
        self.message = message

# ERR-HANDLER позволяет зарегистрировать функцию, которая будет обрабатывать
# те ошибки, которые мы скажем ей и возвращать нужный нам ответ клиенту
@app.errorhandler(HttpError)
def error_handler(error: HttpError):
    response = jsonify({'error': error.message})
    response.status_code = error.status_code
    return response 

# ФУНКЦИЯ ДОБАВЛЕНИЯ ПОЛЬЗОВАТЕЛЯ С ПРОВЕРКОЙ НА ПОВТОРНОЕ ИМЯ С ПОМОЩЬЮ
# СОЗДАННОГО ВЫШЕ ОБРАБОТЧИКА ОШИБОК
# def add_user(session, user):
#     # Добавляем в сессию юзера
#     session.add(session, user)
#     # Обрабатываем ошибку IntegrityError
#     try:
#         # Коминтим изменения
#         session.commit()
#     except IntegrityError as er:
#         raise HttpError(400, "user alredy exist")
# - - - - - - - - - - 
# ПОСЛЕ создания @app.before_request и @app.after_request
# сессии я теперь буду брать из объекта request
# - - - - - - - - - -
def add_user(user):
    # Добавляем в сессию юзера
    request.session.add(user)
    # Обрабатываем ошибку IntegrityError
    try:
        # Коминтим изменения
        request.session.commit()
    except IntegrityError as er:
        raise HttpError(400, "user alredy exist")


# - - - - - - - - - - 
# ФУНКЦИЯ ВАЛИДАЦИИ
# - - - - - - - - - - 
# def validate(schema_cls: type(CreatUser) or type(UpdateUser), json_data):
def validate(schema_cls: type[CreatUser] or type[UpdateUser], json_data):
    '''
    shema_cls - схема проверки входных данных
    json_data - входящий JSON
    '''
    # если произойдет несоответствие скемы входному-му JSON
    try:
        # создаем экземпляр класса заданной схемы и 
        # пробрасываю туда все поля входящего JSON
        # и преобразую в отвалидированный словарь 
        # return schema_cls(**json_data).dict(exclude_unset=True)
        return schema_cls(**json_data).model_dump(exclude_unset=True) # Обновлено в версии >=2.0
        # exclude_unset=True - если я хочу, чтобы в отвалидированном словаре не было значений None,
        # так как во входных данных они могут быть
    except ValidationError as err:
        # можно самому описать ошибку
        # raise HttpError(400, "some data is incorrect")
        # или воспользоваться подробным описанием в pydantic
        errors = err.errors()
        for errors in errors:
            errors.pop("ctx", None) # Удаляем из списка errors поле контекст,
                                # так как оно не валидируется json
        raise HttpError(400, errors)
    pass

# - - - - - - - - - - 
# ПЕРЕНОСИМ ОТКРЫТИЕ СЕССИЙ СЮДА
# Функция которая выполняется перед каждым HTTP-запросом
# - - - - - - - - - - 
@app.before_request
def before_requests():
    session = Session()
    request.session = session # ДОБАВЛЯЕМ СЕССИЮ В САМ request

# После того, как вьюшка (н-р: post()) завершит работу
# нужно закрыть сессию для этого:
@app.after_request # также он позволяет подменить http-ответ, 
                # который возвращает вьюшка (н-р: post()), если это нужно
def affter_request(http_response):
    request.session.close()
    return http_response


# - - - - - - - - - - 
# ДОБАВИМ ФУНКЦИЮ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЯ ПО ID
# - - - - - - - - - - 
def get_user_by_id(user_id) -> User: # возвращает юзера из БД
    # Открываем сессию и .get из нее сущьность User по введенному user_id
    user = request.session.get(User, user_id)
    if user is None:
        raise HttpError(404, "user not found")
    return user

    
# Создаем класс, который реализует логику CRUD 
# для пользователей наследуясьот материнского
# класса MethodView
class UserView(MethodView):
    def get(self, user_id: int):
        # ВЫЗЫВАЕМ ФУНКЦИЮ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЯ ПО ID
        user = get_user_by_id(user_id) 
        return jsonify(user.dict)

    def post(self):
        # Десериализуем строку байтов - b`{JSON}, 
        # прешедшую в запросе от клиента в объект {JSON} (упорядоченный словарь)
        json_data = validate(CreatUser, request.json)
        # - - - - - - - - - - 
        # ПОСЛЕ создания @app.before_request и @app.after_request
        # здесь сессии создавать не нужно
        # - - - - - - - - - - 
        # # Открываем сессию
        # with Session() as session:
        #     user = User(
        #         name=json_data['name'],
        #         password=json_data['password']
        #     )
        #     # - - - - - - - - - - 
        #     # ДОБАВЛЯЕМ ПОЛЬЗОВАТЕЛЯ С ПРОВЕРКОЙ НА ПОВТОРНОЕ ИМЯ С ПОМОЩЬЮ
        #     # СОЗДАННОГО ВЫШЕ ОБРАБОТЧИКА ОШИБОК
        #     # - - - - - - - - - - 
        #     add_user(session, user)
        #     # - - - - - - - - - -
        

        # - - - - - - - - - -
        # ПОСЛЕ создания @app.before_request и @app.after_request 
        # ЗАМЕНЯЕМ НА ЭТОТ КОД
        # - - - - - - - - - -
        # Открываем сессию
        # Поля, JSON-а ("id", "name", "password" и "registration_time"),
        # распоковав его, присваиваем классу User(), сформировав экземпляр класса
        # user - его еще называют объектом user модели Юзер
        # user = User(**json_data)
        # либо так, что одно и тоже
        user = User(
            name=json_data['name'],
            password=hash_password(json_data['password']) # !!!МЫ ЗАПИСЫВАЕМ ПАРОЛЬ В ТОМ ВИДЕ,
                                # КОТОРЫЙ ПРИХОДИТ ОТ КЛИЕНТА ЧТО НЕ БЕЗОПАСНО
                                # ПОЭТОМУ ЕГО НУЖНО ЗАХЕШИРОВАТЬ!!!
                                # И ХРАНИТЬ НЕ В ТОМ ВИДЕ, ЧТО ПРИСЛАЛ КЛИЕНТ, 
                                # А В ХЕШ-ПАРОЛЕ (БУДЕМ ИСПОЛЬЗОВАТЬ АЛГОРИТМ bcrypt)
        )
        # - - - - - - - - - - 
        # ДОБАВЛЯЕМ ПОЛЬЗОВАТЕЛЯ С ПРОВЕРКОЙ НА ПОВТОРНОЕ ИМЯ С ПОМОЩЬЮ
        # СОЗДАННОГО ВЫШЕ ОБРАБОТЧИКА ОШИБОК
        # - - - - - - - - - - 
        add_user(user)
        # - - - - - - - - - -

        # C помощью свойства класса User() - dict, определенного в файле models.py, 
        # преобразуем объект user модели в объект словарь python: user.dict.
        # Сериализуем объект словарь python в байтовую строку - b`{JSON} с помощью функции jsonify()
        # и отправляем ответ клиенту
        return jsonify(user.dict)

    def patch(self, user_id: int):
        # ОБНОВЛЕНИЕ ПОЛЬЗОВАТЕЛЯ
        # Десериализуем строку байтов - b`{JSON}, 
        # прешедшую в запросе от клиента в объект {JSON} (упорядоченный словарь)
        json_data = validate(UpdateUser, request.json) 

        if "password" in json_data:
            json_data['password'] = hash_password(json_data['password'])

        # ВЫЗЫВАЕМ ФУНКЦИЮ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЯ ПО ID ДЛЯ ОБНОВЛЕНИЯ
        user = get_user_by_id(user_id) 
        for field, value in json_data.items():
            setattr(user, field, value) # проставляем пришедшие в запросе 
                            # новые атрибуты пользователю при помощи сеттера
            # добавляем изменеия в БД с проверкой на дублирование имени пользователя
            add_user(user)
        return jsonify(user.dict)


    def delete(self, user_id: int):
        # ВЫЗЫВАЕМ ФУНКЦИЮ ПОЛУЧЕНИЯ ПОЛЬЗОВАТЕЛЯ ПО ID И УДАЛЯЕМ ЕГО
        user = get_user_by_id(user_id) 
        request.session.delete(user)
        request.session.commit() # сохраняем изменения
        return jsonify({"status": "deleted"})


# Преобразовываем класс UserView в представление(вьюшку) 
# для привязки к нему url-ов
user_view = UserView.as_view("user")

# Выполняем роутинг для вьюшки
app.add_url_rule(
    "/user/<int:user_id>", # для "GET", "PATCH", "DELETE"
    view_func=user_view,
    methods=["GET", "PATCH", "DELETE"] 
)
app.add_url_rule(
    "/user", # для "POST"
    view_func=user_view,
    methods=["POST"] 
)

app.run()