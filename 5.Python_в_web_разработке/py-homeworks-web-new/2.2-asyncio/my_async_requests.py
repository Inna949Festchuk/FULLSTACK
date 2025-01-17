import asyncio
import aiohttp
import datetime
from more_itertools import chunked
from my_created_models import init_orm, close_orm, Session, SwapiPeople

MAX_COROUTINS = 5

async def fetch_name(url, session):
    async with session.get(url) as response:
        json_data = await response.json()
        return json_data.get('title') or json_data.get('name')

async def get_people(people_id, session):
    async with session.get(f'http://swapi.py4e.com/api/people/{people_id}') as response:
        json_data = await response.json()

        # Получаем названия фильмов, видов, звездолетов и транспорта
        films = await asyncio.gather(*(fetch_name(film_url, session) for film_url in json_data.get('films', [])))
        species = await asyncio.gather(*(fetch_name(species_url, session) for species_url in json_data.get('species', [])))
        starships = await asyncio.gather(*(fetch_name(starship_url, session) for starship_url in json_data.get('starships', [])))
        vehicles = await asyncio.gather(*(fetch_name(vehicle_url, session) for vehicle_url in json_data.get('vehicles', [])))

        return {
            **json_data,
            'films': films,
            'species': species,
            'starships': starships,
            'vehicles': vehicles
        }

async def insert_to_database(list_json: list[dict]):
    async with Session() as session:
        objects = [
            SwapiPeople(
                id=item.get("id"),
                birth_year=item.get("birth_year"),
                eye_color=item.get("eye_color"),
                films=", ".join(item.get("films", [])),
                gender=item.get("gender"),
                hair_color=item.get("hair_color"),
                height=item.get("height"),
                homeworld=item.get("homeworld"),
                mass=item.get("mass"),
                name=item.get("name"),
                skin_color=item.get("skin_color"),
                species=", ".join(item.get("species", [])),
                starships=", ".join(item.get("starships", [])),
                vehicles=", ".join(item.get("vehicles", []))
            ) for item in list_json
        ]

        # Добавляем все объекты в сессию и коммитим изменения
        session.add_all(objects)
        await session.commit()

async def main():
    await init_orm()

    async with aiohttp.ClientSession() as session:
        tasks = []
        for coroutins_chunk in chunked(range(1, 100), MAX_COROUTINS):
            coroutins = [get_people(i, session) for i in coroutins_chunk]
            tasks.extend(coroutins)  # Собираем все задачи

        # Ожидаем завершения всех задач
        results = await asyncio.gather(*tasks)
        # Создаем задачу для вставки данных в базу и ждем её завершения
        await insert_to_database(results)

    # Закрываем ORM
    await close_orm()

start = datetime.datetime.now()
asyncio.run(main())
print(datetime.datetime.now() - start)




