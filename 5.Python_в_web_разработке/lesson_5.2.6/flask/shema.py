# ВАЛИДАЦИЯ (аналог сериализаторов в django)
from pydantic import BaseModel, field_validator # доп. валидация пароля

# # В виде классов описываются схемы данных, 
# # которым должен соответствовать JSON-словарь запроса

# # У нас будет две схемы:
# # Для проверки JSON для создания пользователя
# class CreatUser(BaseModel):
#     # перечисляем типизированные поля которые ожидаем получить
#     name: str
#     password: str 

#     # дополнительная валидация пароля
#     # ЭТИ ВАЛИДАЦИИ НА ВХОД ПРИНИМАЮТ НЕ self A cls (классы)
#     @field_validator("password")
#     @classmethod # метод экземпляра превращаем в метод класса
#     def check_password(cls, value: str):
#         '''
#         cls - класс
#         value - значения паролей, которые приходят на валидацию
#         '''
#         # Если длина пароля меньше 8 символов, то считать его не безопасным
#         if len(value) < 8:
#             raise ValueError("password is to short")
#         return value


# # Для проверки JSON для обновления пользователя
# class UpdateUser(BaseModel):
#     # Отличие в том что имя и пароль - не обязательные поля
#     name: str | None = None
#     password: str | None = None

#     @field_validator("password")
#     @classmethod # метод экземпляра превращаем в метод класса
#     def check_password(cls, value: str):
#         '''
#         cls - класс
#         value - значения паролей, которые приходят на валидацию
#         '''
#         # Если длина пароля меньше 8 символов, то считать его не безопасным
#         if len(value) < 8:
#             raise ValueError("password is to short")
#         return value

# - - - - - - - - - -
# ЧТОБЫ ИЗБЕЖАТЬ ТАКОГО КОПИПАСТА НУЖНО
# создать базовый класс и наследоваться не от BaseModel,
# а от него, т.е. от BaseUser
# - - - - - - - - - -

class BaseUser(BaseModel):
    password: str

    @field_validator("password")
    @classmethod # метод экземпляра превращаем в метод класса
    def check_password(cls, value: str):
        '''
        cls - класс
        value - значения паролей, которые приходят на валидацию
        '''
        if len(value) < 8:
            raise ValueError("password is to short")
        return value

class CreatUser(BaseUser):
    name: str
    password: str 

class UpdateUser(BaseUser):
    # name: str | None = None
    # password: str | None = None
    name: str or None = None
    password: str or None = None

# Теперь нужно написать функцию, которая будет принимать на ВХОД
# класс схемы и входящий JSON и эта ф-я проверяет, что все правильно, 
# а если нет, то выбросить http-ошибку ЭТО ДОЛАЕМ В ФАЙЛЕ server.py
