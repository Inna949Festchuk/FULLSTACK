import json
# Установить aiohttp и aiohttp[speedups] для быстродействия
# aiohttp ЯВЛЯЕТСЯ ПРОДАКШЕН СЕРВЕРОМ из коробки и его не нужно оборачивать
# в, например, gunicorn
from aiohttp import web

from models import init_orm, close_orm, Session, User # User - класс из БД

# Ошибка
from sqlalchemy.exc import IntegrityError


# Создаем экземпляр класса вебсервера (это наше приложение)
app = web.Application()

# С помощью контекста работы приложения создаем первые записи в БД для ее инициализации
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
        result = await handler(request)
        # Здесь после handler делаем манипуляции
        # Например закрываю сессию в cleanup_ctxс ниже 

        # Добаваляем к объекту request поле session и кладем туда нашу сессию session
        request.session = session

    return result

# После создания контекста его нужно зарегистрировать
app.cleanup_ctx.append(orm_context) # Здесь также закрывается сессия
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
    Добавление нового пользователя
    '''
    session.add(user)
    # Обрабатываем ошибку уникальности пользователя
    try:
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, "user already exists")


# Создаем вьюшку
# с помощбю классов наследуясь от класса View()
class UserView(web.View):

    # Сделаем свойство во вьюшки для возвращения user_id
    # чтобы не копипастить
    @property
    def user_id(self) -> int:
        return int(self.request.match_info["user_id"])
    
    # и возврат сессии
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
        # Создаем экземпляр класса User
        user = User(**json_data) 
        # Добавляем его в сессию
        await add_user(user, self.session)
        # Так как часто нужно возвращать ID  сделаем у модели доп поле dict_id
        # которое вернет JSON айдишника
        return web.json_response(user.dict_id)
        # НУЖНО ЕЩЕ ОТВАЛИДИРОВАТЬ ПОЛЬЗОВАТЕЛЯ (СМ.ЛЕКЦИЮ flask)
        

    async def patch(self):
        pass

    async def delete(self):
        pass



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