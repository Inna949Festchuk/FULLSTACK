import asyncio
import aiohttp

BASE_URL = 'http://localhost:8080'
TOKEN = None

def set_token(token):
    global TOKEN
    TOKEN = token

def get_headers(user_id=None):
    headers = {"Content-Type": "application/json"}
    if TOKEN:
        headers["token"] = TOKEN
    return headers

    
async def add_user(username, password, email=None):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f'{BASE_URL}/user',
            json={'name': username, 'password': password, 'email': f'{username}@test.com' if email is None else email},
        )
        print(response.status)
        print(await response.text())

async def get_user(user_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f'{BASE_URL}/user/{user_id}',
            headers=get_headers()
        )
        print(response.status)
        print(await response.text())

async def update_user(user_id, password=None, email=None):
    async with aiohttp.ClientSession() as session:
        json_data = {}
        if password is not None:
            json_data['password'] = password
        if email is not None:
            json_data['email'] = email
        response = await session.patch(
            f'{BASE_URL}/user/{user_id}',
            json=json_data,
            headers=get_headers()
        )
        print(response.status)
        print(await response.text())

async def delete_user(user_id):
    async with aiohttp.ClientSession() as session:
        response = await session.delete(
            f'{BASE_URL}/user/{user_id}',
        )
        print(response.status)
        print(await response.text())

async def get_ad(ad_id):
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f'{BASE_URL}/ad/{ad_id}',
        )
        print(response.status)
        print(await response.text())

async def get_all_ads():
    async with aiohttp.ClientSession() as session:
        response = await session.get(
            f'{BASE_URL}/ad',
        )
        print(response.status)
        print(await response.text())

async def post_ad(title, description, user_id=1):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f'{BASE_URL}/ad',
            json={'title': title, 'description': description},
            headers=get_headers()
        )
        print(response.status)
        print(await response.text())


async def update_ad(ad_id, title=None, description=None, user_id=None):
    async with aiohttp.ClientSession() as session:
        json_data = {}
        if title is not None:
            json_data['title'] = title
        if description is not None:
            json_data['description'] = description
        if user_id is not None:
            json_data['user_id'] = user_id
        response = await session.patch(
            f'{BASE_URL}/ad/{ad_id}',
            json=json_data,
        )
        print(response.status)
        print(await response.text())

async def delete_ad(ad_id):
    async with aiohttp.ClientSession() as session:
        response = await session.delete(
            f'{BASE_URL}/ad/{ad_id}',
        )
        print(response.status)
        print(await response.text())

async def login_user(username, password):
    async with aiohttp.ClientSession() as session:
        response = await session.post(
            f'{BASE_URL}/login',
            json={'name': username, 'password': password},
        )
        response = await response.json()
        if 'token' in response:
            global TOKEN
            TOKEN = response['token']
        # user_id = response['user_id']
        # print(user_id)
        # print(TOKEN)


if __name__ == '__main__':
    # asyncio.run(add_user('user_4', 'password'))
    asyncio.run(login_user('user_1', 'password'))
    print(TOKEN)
    # asyncio.run(login_user('user_2', 'password'))
    # asyncio.run(login_user('user_3', 'password'))
    # asyncio.run(get_user(3))
    asyncio.run(update_user(3, password='new_password', email='new_email@test.com'))
    # asyncio.run(get_all_ads())
    # asyncio.run(get_ad(1))
    # asyncio.run(post_ad('title1', 'description1'))
    # asyncio.run(update_ad(1, title='new_title1', description='new_description1'))
    # asyncio.run(delete_ad(2))