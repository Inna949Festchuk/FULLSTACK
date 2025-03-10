# Асинхронный подход
import asyncio # Для запуска асинхронного кода в приложении


async def get_people(people_id):

    return 42

# get_people_coroutine = get_people(4)
# print(f'{get_people_coroutine=}') 

# out: объект асинхронной функции - КОРУТИНА <coroutine object get_people at 0x000000000067A4C0>

# Чтобы функции выполнялись асинхронно их нужно
# вызывать в event loop (цикле событий)
# Можно сказать, что корутины помещаются в цикл событий

# Чтобы НЕМЕДЛЕННО извлечь из 
# результата асинхронной функции (корутины) ее значение
# нужно использовать БЛОКИРУЮЩЕЕ ключевое слово await 

async def main():

    response = await get_people(4) # значение корутины
    print(f'{response=}')

asyncio.run(main()) # run() - это метод создающий цикл событий event loop  
#  в цикл событий передается main() для вызова асинхронных функций

# out:
# response=42