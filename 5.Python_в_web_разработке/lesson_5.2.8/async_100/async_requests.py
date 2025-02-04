import asyncio
import datetime

import aiohttp
from more_itertools import chunked

from models import Session, SwapiPeople, close_orm, init_orm

MAX_COROS = 5


async def get_people(people_id, session):
    response = await session.get(f"https://swapi.py4e.com/api/people/{people_id}/")
    json_data = await response.json()
    return json_data


async def insert_to_database(list_json: list[dict]):
    async with Session() as session:
        objects = [SwapiPeople(json=item) for item in list_json]
        session.add_all(objects)
        await session.commit()


async def main():
    await init_orm()

    async with aiohttp.ClientSession() as session:
        for coros_chunk in chunked(range(1, 100), MAX_COROS):
            coros = [get_people(i, session) for i in coros_chunk]
            result = await asyncio.gather(*coros)
            asyncio.create_task(insert_to_database(result))
    tasks = asyncio.all_tasks()
    current_task = asyncio.current_task()
    tasks.remove(current_task)
    await asyncio.gather(*tasks)
    await close_orm()


start = datetime.datetime.now()
main_coro = main()
asyncio.run(main_coro)
print(datetime.datetime.now() - start)
