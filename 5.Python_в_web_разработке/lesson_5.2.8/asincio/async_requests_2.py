# Асинхронный подход (продолжение)
import asyncio


async def get_people(people_id):

    return 42

async def main():
    # так код всеравно будет выполняться синхронно
    response_1 = await get_people(1)
    response_2 = await get_people(2)
    response_3 = await get_people(3)
    response_4 = await get_people(4)
    print(response_1, response_2, response_3, response_4)
    # так код будет выполняться асинхронно (конкурентно)
    coroutine_1 = get_people(1)
    coroutine_2 = get_people(2)
    coroutine_3 = get_people(3)
    coroutine_4 = get_people(4)
    # gather() в цикле событий event loop 
    # проверяет выполнение АСИНХРОННЫХ ФУНКЦИЙ
    # и после того, как какая-то из них выполнилась
    # складывает ее КОРУТИНУ в список.

    # Поскольку gather() - это тоже асинхронная функция
    # чтобы извлечь из ее корутины результат (список значений)
    # нужно применить ключевое слово await 
    result = await asyncio.gather(coroutine_1, coroutine_2, coroutine_3, coroutine_4)
    print(result)

asyncio.run(main()) 