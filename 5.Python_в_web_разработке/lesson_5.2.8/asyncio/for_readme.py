import asyncio

async def asyncfoo(name, delay):
    await asyncio.sleep(delay)
    return f'asyncfoo {name} complete'

async def main():
    # Использование gather
    results = await asyncio.gather(asyncfoo('A', 2), asyncfoo('B', 1))
    print(results)

    # Использование create_task
    task_c = asyncio.create_task(asyncfoo('C', 3))
    # Здесь можно выполнять другие операции
    print("Делаю что-то еще, пока выполняется C...")
    await task_c
    print("C complete")

asyncio.run(main())

# ### Вывод
# - Используйте `asyncio.gather`, когда нужно собирать результаты сразу 
# от нескольких асинхронных функций.
# - Используйте `asyncio.create_task`, когда хотите управлять жизненным 
# циклом отдельных асинхронных функций и выполнять другие операции параллельно. 
