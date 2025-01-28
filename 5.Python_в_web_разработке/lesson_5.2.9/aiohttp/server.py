# Установить aiohttp и aiohttp[speedups] для быстродействия
# aiohttp ЯВЛЯЕТСЯ ПРОДАКШЕН СЕРВЕРОМ из коробки и его не нужно оборачивать
# в, например, gunicorn
from aiohttp import web

# Создаем экземпляр класса вебсервера (это наше приложение)
app = web.Application()

# Создаем вьюшку
# async def hello_world(request: web.Request): # Объект request это экземпляр класса web.Request
#     response = web.json_response({"hello": "world"}) # это аналог jsonyfi
#     return response

async def hello_world(request: web.Request): 
    # match_info - это словарик куда падают переменные из url
    some_id = int(request.match_info['some_id'])
    # получаем значение из querystring
    qs = request.query
    # получаем заголовки
    headers = request.headers
    # получаем json
    json_data = await request.json()
    print(f"{some_id=}")
    print(f"{qs=}")
    print(f"{headers=}")
    print(f"{json_data=}")    
    response = web.json_response({"hello": "world"}) # это аналог jsonyfi
    return response


# Привязываем вьюшку к url
app.add_routes([
    # web.post("/hello/world", hello_world)
    web.post("/hello/world/{some_id:\d+}", hello_world) # Во flask можно задавать тип ожидаемой из url переменной
                                                        # В aiohttp так нельзя и все задается регулярками
])

# Для запуска сервера нужно 
# Внутри создается Event loop в него кладется наше приложение и стартует
web.run_app(app)