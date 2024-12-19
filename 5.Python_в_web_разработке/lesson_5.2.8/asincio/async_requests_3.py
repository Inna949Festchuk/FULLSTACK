# Асинхронный подход (продолжение)
import asyncio
# Библиотеку requests использовать мы не можем, т.к.
# чтобы асинхронные функции давали выигрышь 
# они должны использоваться с другими асинхронными ф-ями,
# которые поставляются в специальных библиотеках
# аналогом библиотеки requests является библиотека aiohttp
import aiohttp

import datetime

from more_itertools import chunked


async def get_people(people_id, session):
    # Отправляем запрос и получаем значение корутины с пом. await
    response = await session.get(f'http://swapi.py4e.com/api/people/{people_id}')
    # Десериализуем. Получаем json. Ф-я тоже асинхронная (вообще
    # все ф-ии работы с сетью асинхронные)
    json_data = await response.json()
    return json_data

# Разделяем всю последовательность запросов на подпоследовательности
# чтобы не переполнить оперативку и не задедосить сервак
MAX_COROTINS = 5

async def main():
    # Создаем сессию
    # session = aiohttp.ClientSession()
        # for coroutins_chunk in chunked(range(1, 100), MAX_COROTINS):
        #     coroutins = [get_people(i, session) for i in coroutins_chunk]
        #     result = await asyncio.gather(*coroutins)
        #     print(result)
    # await session.close()
    
    # Так как объект сессии является асинхронным менеджером контекста 
    # можно заменить так
    
    # Создаем сессию
    async with aiohttp.ClientSession() as session:
        # выгружаем 100 персонажей асинхронно (конкурентно)
        # разделяем последовательность из 100 элементов на подпоследовательности по 5 элементов
        for coroutins_chunk in chunked(range(1, 100), MAX_COROTINS):
            coroutins = [get_people(i, session) for i in coroutins_chunk]
            result = await asyncio.gather(*coroutins)
            print(result)

start = datetime.datetime.now()
asyncio.run(main()) 
print(datetime.datetime.now() - start)
