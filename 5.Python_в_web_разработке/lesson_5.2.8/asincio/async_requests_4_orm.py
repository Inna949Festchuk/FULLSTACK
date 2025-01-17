# Асинхронный подход (продолжение:выгружаем в ORM)
import asyncio
import aiohttp
import datetime

from more_itertools import chunked

# Импортируем из models.py инициализацию и закрытие БД
# фабрику сессий и нашу модель
from models import init_orm, close_orm, Session, SwapiPeople

MAX_COROTINS = 5

async def get_people(people_id, session):
    response = await session.get(f'http://swapi.py4e.com/api/people/{people_id}')
    # response = await session.get(f'http://127.0.0.1:5000/press/{people_id}')
    json_data = await response.json()
    return json_data

# Пишем функцию для вставки в БД значений списка result gather-а, 
# содержащего пять вложенных JSON (это будут отдельные экземпляры ORM-модели) 
async def insert_to_database(list_json: list[dict]):
    # # открываем сессию
    # async with Session() as session:
    #     objects = []
    #     for item in list_json:
    #         # Создаем экземпляр SwapiPeople и кладем в него JSON
    #         swapi = SwapiPeople(json=item)
    #         objects.append(swapi)
    #     # Добавляем все объекты в сессию
    #     session.add_all(objects)
    #     # Комиттимся
    #     await session.commit()

    # Перерписываем этот код с помощью компрекейшн выражения
    async with Session() as session:
        objects = [SwapiPeople(json=item) for item in list_json]
        session.add_all(objects)
        await session.commit()


async def main():
    # Инициализируем orm
    await init_orm()

    async with aiohttp.ClientSession() as session:
        for coroutins_chunk in chunked(range(1, 100), MAX_COROTINS):
            
            coroutins = [get_people(i, session) for i in coroutins_chunk]
            result = await asyncio.gather(*coroutins) # ждем завершения формирования пятерки JSON-ов
            
            # Вставляем result в БД

            # await insert_to_database(result)

            # Используя асинхронные инструменты оптимизируем эту часть кода
            # await - это БЛОКИРУЮЩАЯ операция,
            # но ведь мы можем асинхронно начать выгружать с сервера 
            # следующую пятерку JSON-ов не дожидаясь вставки 
            # в БД предыдущих выгруженных
           
            # Это можно организовать с помощью объекта пайтона Task (ЗАДАЧА):
            # Задаем в методе create_task объект корутину insert_to_database(result)

            asyncio.create_task(insert_to_database(result)) # НЕ ЖДЕМ ЗАВЕРШЕНИЯ ЗАПИСИ В БД
            
            # !!! ОПЕРАЦИЯ СОЗДАНИЯ КОРУТИНЫ ТЕПЕРЬ НЕ БЛОКИРУЮЩАЯ !!!
            # !!! И ПЕРЕД asyncio.create_task() НЕТ БЛОК. ОПЕРАЦИИ await !!!
            # !!! В ОТЛИЧАЕ ОТ await asyncio.gather() !!!

            # Таким образом операция вставки в БД начинает выполняться, 
            # но при этом мы продолжаем выполнять код дальше (начинаем 
            # формировать сльедующую пятерку JSON-ов)
            # НЕ ДОЖИДАЯСЬ ЗАВЕРШЕНИЯ ВЫПОЛНЕНИЯ ОПЕРАЦИИ ВСТАВКИ В БД

            print(result)

    # ЕЩЕ ОДНА ПРОБЛЕМА асинхронного кода - последние 5 JSON-ов не попали в БД. 
    # Это происходит потому, что последния задача вставки в БД insert_to_database(result)
    # не успевает завершиться, а сессия orm уже закрывается, 
    # можно попробывать дождаться завершения выполнения 
    # последней задачи insert_to_database(result) применением await task, 
    
    # await task # ждем завершения последней задачи вставки в БД insert_to_database(result)

    # но тогда может не успеть завершиться
    # предпоследняя задача insert_to_database(result), 
    # которая по времени выполнения будет дольше  
    
    # !!! В этом ОСОБЕННОСТЬ АСИНХРОННОГО КОДА -
    # мы никогда не знаем наверняка когда асинхронная функция завершиться !!!
    # а пайтон никогда не ждет завершения функций

    # КАК ГАРАНТИРОВАТЬ ВЫПОЛНЕНИЕ ЗАДАЧ?
    tasks = asyncio.all_tasks()

    # Это функция обращается к текущему event loop и забирает из него все незавершенные задачи,
    # т.е. те, что еще выполняются сейчас и выгружает эти задачи в виде множества.

    # print(tasks)

    # out: 
    # {
    #     <Task pending name='Task-1' coro=<main() running at async_requests_4_orm.py:96> cb=[_run_until_complete_cb() at C:\Users\GIS27\AppData\Local\Programs\Python\Python38\lib\asyncio\base_events.py:184]>, 
    #     <Task pending name='Task-239' coro=<insert_to_database() running at async_requests_4_orm.py:39>
    #     wait_for=<Future pending cb=[BaseProtocol._on_waiter_completed(), <TaskWakeupMethWrapper object at
    #     0x00000000056B8400>()]>>
    # }

    # Дальше мы можем снова закинуть их в гезер и выполнить с завершением конкурентно,
    # но туда же попадет и сама асинхронная функция main() (см. out выше)
    # и наше приложение зацикливается - мы получаем РЕКУРСИЮ
    
    # Поэтому сначала получаем текущую задачу main()
    current_task = asyncio.current_task()
    # и далее из множества задач tasks удаляю ее
    tasks.remove(current_task)

    # print(tasks)
    # out:
    # {
    #     <Task pending name='Task-239' coro=<insert_to_database() running at async_requests_4_orm.py:39> wait_for=<Future pending cb=[BaseProtocol._on_waiter_completed(), <TaskWakeupMethWrapper object at 0x00000000056BA460>()]>>
    # }

    # Теперь в гезере мы конкурентно выполняем с завершением  
    # все текущие невыполненные задачи кроме main()
    await asyncio.gather(*tasks)
           
    # Закрываем сессию orm
    await close_orm()

start = datetime.datetime.now()
asyncio.run(main()) 
print(datetime.datetime.now() - start)

