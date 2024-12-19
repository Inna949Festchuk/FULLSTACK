# Асинхронный подход
import asyncio # Для запуска асинхронного кода в приложении


async def get_people(people_id):

    return 42

# get_people_coroutine = get_people(4)
# print(f'{get_people_coroutine=}') 

# out: объект асинхронной функции - КОРУТИНА <coroutine object get_people at 0x000000000067A4C0>
# Асинхронные функции можно вызывать в event loop (цикле событий), где по мере
# их выполнения (готовности) возвращать значения их корутин


# Чтобы НЕМЕДЛЕННО извлечь из 
# результата асинхронной функции (корутины) ее значение
# нужно использовать ключевое слово await (В СВОЮ ОЧЕРЕДЬ его можно
# использовать только внутри асинхронной функции main())

async def main():

    response = await get_people(4) # значение корутины
    print(f'{response=}')

asyncio.run(main()) # run() - это цикл событий event loop и 
#  в него передаются все значения корутин, которые будут возвращаться main()

# out:
# response=42