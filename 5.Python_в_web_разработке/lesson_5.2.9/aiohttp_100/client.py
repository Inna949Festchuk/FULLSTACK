import asyncio

import aiohttp


async def main():

    async with aiohttp.ClientSession() as session:
        # response = await session.post(
        #     "http://127.0.0.1:8080/user",
        #     json={
        #         "name": "user_2",
        #         "password": "1234"
        #     }
        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.get(
        #     "http://127.0.0.1:8080/user/1000",
        # )
        # print(response.status)
        # print(await response.json())

        # response = await session.patch(
        #     "http://127.0.0.1:8080/user/1",
        #     json={
        #         "name": "new name"
        #     }
        # )
        # print(response.status)
        # print(await response.json())

        response = await session.delete(
            "http://127.0.0.1:8080/user/1",
        )
        print(response.status)
        print(await response.json())

        response = await session.get(
            "http://127.0.0.1:8080/user/1",
        )
        print(response.status)
        print(await response.json())


asyncio.run(main())
