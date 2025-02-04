import json
# Установить aiohttp и aiohttp[speedups] для быстродействия
# aiohttp ЯВЛЯЕТСЯ ПРОДАКШЕН СЕРВЕРОМ из коробки и его не нужно оборачивать
# в, например, gunicorn
from aiohttp import web

from models import init_orm, close_orm, Session, User # User - класс из БД

# Ошибка
from sqlalchemy.exc import IntegrityError

# Используем bcrypt для хеширования передаваемых паролей как во flask 
# но там была bcrypt адаптированная для flask а тут стандартная 
from bcrypt import hashpw, checkpw, gensalt

# Создаем экземпляр класса вебсервера (это наше приложение)
app = web.Application()



# Шифруем пароль
def hash_password(password: str) -> str:
    password_bytes = password.encode() # Приобразуем пароль в байты
    # Эти байты засовываем в метод bcrypt.hashpw
    hashed_password_bytes = hashpw(password_bytes, gensalt())
    # gensalt - так наз. СОЛЬ - случайные байты, которые добавятся к паролю
    # Преобразуем возвращенные байты обратно в строчку - хешированный пароль
    hashed_password = hashed_password_bytes.decode()
    return hashed_password

# Функци проверки пароля
def check_password(password: str, hashed_password: str) -> bool:
    '''
    Функци проверки пароля сравнивает пароль клиента 
    с захешированным паролем который лежит в БД
    '''
    # Прелбразуем оба пароля в байты
    password_bytes = password.encode()
    hashed_password_bytes = hashed_password.encode()
    return checkpw(password_bytes, hashed_password_bytes)



# С помощью контекста работы приложения создаем начальные записи в БД
async def orm_context(app):
    # Все что написано до yield выполнится при старте приложения
    print("START")
    await init_orm() # Инициализация ORM при старте прил-я
    yield
    # Все что написано после yield выполнится при завершении работы приложения
    print("FINISH")
    await close_orm() # Закрытие ORM при завершении прил-я


# Пишем MIDDLEWARE - это ф-я внутри которой выполняется http-запрос
# В MIDDLEWARE пишется то что мы хотим сделать до выполнения http-запроса
# и после выполнения http-запроса
# Внутри MIDDLEWARE должна открываться сессия

@web.middleware # Регистрируем MIDDLEWARE(1 ЭТАП)
async def session_middleware(request: web.Request, handler): 
    '''
    request: web.Request - объект запроса, тот же самый который падает во вьюшку
    handler - это вьюшка которая будет выполняться
    '''
    # Здесь до handler делаем манипуляции
    # Например, открываю сессию
    async with Session() as session:
        #  Добаваляем к объекту request поле session и кладем туда нашу сессию session
        request.session = session
        result = await handler(request)
        # Здесь после handler делаем манипуляции
        # Например закрываю сессию в cleanup_ctxс ниже 
        
    return result

# После создания контекста его нужно зарегистрировать
app.cleanup_ctx.append(orm_context) # Здесь закрывается сессия

# После создания MIDDLEWARE его нужно зарегистрировать (2 ЭТАП)
app.middlewares.append(session_middleware)

# ОБОРАЧИВАЕМ КОД ПОЛУЧЕНИЯ ОШИБОК В ФУНКЦИЮ
def get_http_error(error_cls, message):
    '''
    error_cls - класс ошибки который мы хотим выцбросить, н-р HTTPNotFound
    message - сообщение ошибки
    '''
    message = {"error": message}
    message = json.dumps(message)
    error = error_cls(text=message, content_type="application/json")
    raise error


# Ф-я для взаимодействия с базой данных
async def get_user_by_id(user_id: int, session: Session) -> User:
    '''
    Получение пользователя по его ID
    '''
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, "user not found")
    return user

async def add_user(user: User, session: Session):
    '''
    Добавление пользователя по его ID
    '''
    session.add(user) # Добавляем в БД 
    # Обрабатываем ошибку уникальности пользователя при записи в БД
    try: 
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, "user already exists")

async def delete_user(user: User, session: Session):
    '''
    Удаление пользователя по его ID
    '''
    await session.delete(user)
    await session.commit()

# Создаем вьюшку
# с помощбю классов наследуясь от класса View()
class UserView(web.View):

    # Сделаем свойство во вьюшки для возвращения user_id
    # чтобы не копипастить
    @property
    def user_id(self) -> int:
        return int(self.request.match_info["user_id"])
    
    # или возврат сессии
    @property
    def session(self) -> Session:
        return self.request.session

    async def get(self):
        # ОБОРАЧИВАЕМ КОД ПОЛУЧЕНИЯ ОШИБОК В ФУНКЦИЮ
        # - - - - - - - - - - - - - - -  
        # # Теперь чтобы воспользоваться сессией я вытаскиваю объек request и из него нашу сессию,
        # # которая в нем лежит
        # self.request.session
        # # Выбрасываем ошибки например 404 c какой-то инфой
        # # для этого в REST нужно сформировать словарь 
        # # и спомощью ббиблиотеки json преобразовать словаро в JSON
        # json_response = {"error": "user not found"}
        # json_response = json.dumps(json_response)
        # raise web.HTTPNotFound(text=json_response, content_type="application/json")
        # # для того чтобы клиент понимал что мы передаем JSON 
        # # мы также должны сформировать соответствующий заголовок content_type
        # - - - - - - - - - - - - - - - 
        
        # raise get_http_error(web.HTTPConflict, "incorrect format")
        # - - - - - - - - - - - - - - - 
        
        # Взаимодействуем с БД
        # user_id = self.request.match_info["user_id"]
        # user = await get_user_by_id(int(user_id), self.rtequest.session)
        # # self.rtequest.session - потомучто отработает MIDDLEWARE

        # Применим созданные выше свойства вьюшки self.user_id и self.session
        user = await get_user_by_id(self.user_id, self.session)

        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json() # извлекаем из запроса json

        # Предпологаем что JSON содержит пароль (проверяем валидацией)
        # Хешируем пароль
        json_data['password'] = hash_password(json_data['password'])

        # Создаем экземпляр класса User
        user = User(**json_data) 
        # Добавляем его в сессию
        await add_user(user, self.session)
        # Так как часто нужно возвращать ID  сделаем у модели доп поле dict_id
        # которое вернет JSON айдишника
        return web.json_response(user.dict_id)
        # НУЖНО ЕЩЕ ОТВАЛИДИРОВАТЬ ПОЛЬЗОВАТЕЛЯ с пом. pydantic (СМ.ЛЕКЦИЮ flask)
        

    async def patch(self):
        user = await get_user_by_id(self.user_id, self.session)

        json_data = await self.request.json() # Если прийдет {"name": "Anton"}

        # Проверяем если пришел пароль на обновление то нужно его захешировать
        if "password" in json_data:
            json_data['password'] = hash_password(json_data['password'])

        # проходим по полям в JSON и прописываем атрибуты нашему пользователю
        for field, value in json_data.items():
            # Устанавливаем для user-а в поле field - name, а в value - Anton
            setattr(user, field, value) # Т.о. у юзера имя обновится на Антон
        # Записываем изменения в БД
        await add_user(user, self.session) # Записываем изменения в БД
        return web.json_response(user.dict_id) # Возвращаем адишник обновленной записи

    async def delete(self):
        user = await get_user_by_id(self.user_id, self.session)
        await delete_user(user, self.session)
        return web.json_response({"status": "success"})


# Привязываем вьюшку к url
app.add_routes([

    web.post("/user", UserView), 

    web.get("/user/{user_id:\d+}", UserView),
    web.patch("/user/{user_id:\d+}", UserView),
    web.delete("/user/{user_id:\d+}", UserView)   
])

# Для запуска сервера нужно 
# Внутри создается Event loop в него кладется наше приложение и стартует
web.run_app(app)