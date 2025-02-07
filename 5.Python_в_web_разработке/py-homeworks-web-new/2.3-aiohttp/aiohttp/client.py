import aiohttp
import asyncio

async def main():
    # Создаем сессию
    async with aiohttp.ClientSession()  as session:
        response = await session.post(
            "http://127.0.0.1:8080/press",
            json={
                "title": "Первое объявление", 
                "body": "Продам кота", 
                "onwer": "Иванов А.А."
            }
        )
        print(response.status)
        print(await response.json())

        # - - - - - - - - - - -

        # response = await session.get(
        #     "http://127.0.0.1:8080/press/1"
        # )
        # print(response.status)
        # print(await response.json())

        # - - - - - - - - - - -

        # response = await session.patch(
        #     "http://127.0.0.1:8080/press/1",
        #     json={
        #         "title": "Первое объявление", 
        #         "body": "Продам РЫЖЕГО кота", 
        #         "onwer": "Иванов А.А."
        #     }
        # )
        # print(response.status)
        # print(await response.json())
        
        # response = await session.get(
        #     "http://127.0.0.1:8080/press/1"
        # )
        # print(response.status)
        # print(await response.json())

        # - - - - - - - - - - -
        # response = await session.delete(
        #     "http://127.0.0.1:8080/press/1"
        # )
        # print(response.status)
        # print(await response.json())
        
        # response = await session.get(
        #     "http://127.0.0.1:8080/press/1"
        # )
        # print(response.status)
        # print(await response.json())

        # - - - - - - - - - - -

# Запускаем приложение
asyncio.run(main())