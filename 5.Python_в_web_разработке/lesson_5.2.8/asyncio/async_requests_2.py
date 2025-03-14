# Асинхронный подход (продолжение)
import asyncio


async def get_people(people_id):

    return 42

async def main():
    # так код всеравно будет выполняться синхронно
    # потому что await не только извлекает значение объекта корутины, но и
    # одновременно выступает как БЛОКИРУЮЩЕЕ слово, т.е. пока 
    # асинхронная функция не отработает следующая выполняться не начнет
    response_1 = await get_people(1) # начинает выполняться
    response_2 = await get_people(2) # ждет завершения предыдущей и начинает выполняться
    response_3 = await get_people(3) # ждет завершения предыдущей и начинает выполняться
    response_4 = await get_people(4) # ждет завершения предыдущей и начинает выполняться
    print(response_1, response_2, response_3, response_4)

    # так код будет выполняться асинхронно,
    # выполнение всех функций СТАРТУЕТ практически ОДНОМОМЕНТНО,
    # при этом есть риск, что мы можем не дождаться окончания выполнения
    # некоторых особо долгих из них, продолжив выполнять код дальше и 
    # в конечном итоге получить ошибку (например не успеть записать
    # предыдущий результат в БД, см. пояснения в async_requests_4_orm.py)
    coroutine_1 = get_people(1) # начинает выполняться
    coroutine_2 = get_people(2) # начинает выполняться
    coroutine_3 = get_people(3) # начинает выполняться
    coroutine_4 = get_people(4) # начинает выполняться

    # gather() в цикле событий event loop 
    # проверяет выполнение АСИНХРОННЫХ ФУНКЦИЙ, 
    
    # и КОНКУРЕНТНО, по мере ГАРАНТИРОВАННОГО завершения 
    # их выполнения, складывает результат - 
    # значения их объектов КОРУТИН в список.    

    result = await asyncio.gather(coroutine_1, coroutine_2, coroutine_3, coroutine_4)
    # Поскольку gather() - это тоже асинхронная функция
    # чтобы извлечь из ее корутины результат (список значений)
    # нужно применить блокирующую операцию await 
    print(result)
    # out: [42, 42, 42, 42]

# Передаем main() в цикл событий event loop,
# который создается с помощью метода run() 
asyncio.run(main()) 