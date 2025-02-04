# Дляотправки запросов можно использовать клиентскую часть
# библиотеки aiohttp хотя можно и requests
import aiohttp
import asyncio

# async def main():
#     # Создаем сессию
#     async with aiohttp.ClientSession()  as session:
#         # response = await session.get("http://127.0.0.1:8080")
#         response = await session.post("http://127.0.0.1:8080/hello/world")
#         print(response.status)
#         # print(await response.text())
#         print(await response.json())

# Клиент может передавать информацию на сервер в след.виде:
# - переменниые в самом url "http://127.0.0.1:8080/hello/world/42"
# - json
# - querystring "http://127.0.0.1:8080/hello/world/42?param1=val1&param2=val2"
# - heders

# # ПЕРЕДАЕМ ПЕРЕМЕННУЮ В url
# async def main():
#     # Создаем сессию
#     async with aiohttp.ClientSession()  as session:
#         # response = await session.get("http://127.0.0.1:8080")
#         response = await session.post(
#             "http://127.0.0.1:8080/hello/world/42?param1=val1&param2=val2",
#             json={
#                 "name": "Amily",
#                 "surname":"Simpson"
#             },
#             headers={
#                 "token": "xxxxx"
#             }
#         )
#         print(response.status)
#         # print(await response.text())
#         print(await response.json())


async def main():
    # Создаем сессию
    async with aiohttp.ClientSession()  as session:
        response = await session.post(
            "http://127.0.0.1:8080/user",
            json={
                "name": "user_2",
                "password":"1234"
            }
        )
        print(response.status)
        print(await response.json())

        # - - - - - - - - - - -

        # response = await session.get(
        #     "http://127.0.0.1:8080/user/1"
        # )
        # print(response.status)
        # print(await response.json())

        # - - - - - - - - - - -

        # response = await session.patch(
        #     "http://127.0.0.1:8080/user/1",
        #     json={
        #         "name": "new_user",
        #         "password":"1234"
        #     }
        # )
        # print(response.status)
        # print(await response.json())
        
        # response = await session.get(
        #     "http://127.0.0.1:8080/user/1"
        # )
        # print(response.status)
        # print(await response.json())

        # - - - - - - - - - - -
        # response = await session.delete(
        #     "http://127.0.0.1:8080/user/1"
        # )
        # print(response.status)
        # print(await response.json())
        
        # response = await session.get(
        #     "http://127.0.0.1:8080/user/1"
        # )
        # print(response.status)
        # print(await response.json())

        # - - - - - - - - - - -

# Запускаем приложение
asyncio.run(main())