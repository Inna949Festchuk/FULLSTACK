# Асинхронный подход (продолжение)
import asyncio


async def get_people(people_id):

    return 42

async def main():
    # так код всеравно будет выполняться синхронно
    # потому что await не только извлекает значение корутины, но и
    # одновременно выступает как БЛОКИРУЮЩЕЕ слово, т.е. пока 
    # асинхронная функция не отработает следующая выполняться не начнет
    response_1 = await get_people(1)
    response_2 = await get_people(2)
    response_3 = await get_people(3)
    response_4 = await get_people(4)
    print(response_1, response_2, response_3, response_4)

    # так код будет выполняться асинхронно,
    # но есть риск, что мы можем не дождаться окончания выполнения
    # некоторых особо долгих из них, продолжив выполнять код дальше и 
    # в конечном итоге получить ошибку 
    coroutine_1 = get_people(1)
    coroutine_2 = get_people(2)
    coroutine_3 = get_people(3)
    coroutine_4 = get_people(4)

    # gather() в цикле событий event loop 
    # проверяет выполнение АСИНХРОННЫХ ФУНКЦИЙ, 
    
    # и КОНКУРЕНТНО, по мере их выполнения, 
    # складывает их КОРУТИНЫ в список.

    result = await asyncio.gather(coroutine_1, coroutine_2, coroutine_3, coroutine_4)
    # Поскольку gather() - это тоже асинхронная функция
    # чтобы извлечь из ее корутины результат (список значений)
    # нужно применить ключевое слово await 
    print(result)

# Помещаем main() в цикл событий event loop
asyncio.run(main()) 