import datetime
import json
from typing import Type, Callable, Awaitable

from auth import hash_password, check_password

from aiohttp import web
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


from config import PG_DSN, TOKEN_TTL
from models import Base, User, Token


engine = create_async_engine(PG_DSN)

Session = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

ERROR_TYPE = Type[web.HTTPUnauthorized] | Type[web.HTTPForbidden] | Type[web.HTTPNotFound]


def raise_http_error(error_class: ERROR_TYPE, message: str | dict):
    raise error_class(
        text=json.dumps({"status": "error", "description": message}),
        content_type="application/json",
    )


async def get_orm_item(item_class: Type[User] | Type[Token], item_id: int | str, session: Session) -> User | Token:
    item = await session.get(item_class, item_id)
    if item is None:
        raise raise_http_error(web.HTTPNotFound, f"{item_class.__name__} not found")

    return item


@web.middleware
async def session_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    async with Session() as session:
        request["session"] = session
        return await handler(request)


@web.middleware
async def auth_middleware(
    request: web.Request, handler: Callable[[web.Request], Awaitable[web.Response]]
) -> web.Response:
    token_id = request.headers.get("token")
    if not token_id:
        raise_http_error(web.HTTPForbidden, "incorrect token")
    try:
        token = await get_orm_item(Token, token_id, request["session"])
    except web.HTTPNotFound:
        token = None
    if not token or token.creation_time + datetime.timedelta(seconds=TOKEN_TTL) <= datetime.datetime.now():
        raise_http_error(web.HTTPForbidden, "incorrect token")
    request["token"] = token
    return await handler(request)


def check_owner(request: web.Request, user_id: int):
    if not request["token"] or request["token"].user.id != user_id:
        raise_http_error(web.HTTPForbidden, "only owner has access")


async def login(request: web.Request):
    login_data = await request.json()
    query = select(User).where(User.name == login_data["name"])
    result = await request["session"].execute(query)
    user = result.scalar()
    if not user or not check_password(login_data["password"], user.password):
        raise_http_error(web.HTTPUnauthorized, "incorrect login or password")

    token = Token(user=user)
    request["session"].add(token)
    await request["session"].commit()

    return web.json_response({"token": str(token.id)})


class UserView(web.View):
    async def get(self):
        user_id = int(self.request.match_info["user_id"])
        user = await get_orm_item(User, user_id, self.request["session"])
        return web.json_response(
            {"id": user.id, "name": user.name, "creation_time": int(user.creation_time.timestamp())}
        )

    async def post(self):
        user_data = await self.request.json()
        user_data["password"] = hash_password(user_data["password"])
        new_user = User(**user_data)
        self.request["session"].add(new_user)
        await self.request["session"].commit()
        return web.json_response({"id": new_user.id})

    async def patch(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user_data = await self.request.json()
        if "password" in user_data:
            user_data["password"] = hash_password(user_data["password"])

        user = await get_orm_item(User, user_id, self.request["session"])
        for field, value in user_data.items():
            setattr(user, field, value)
        self.request["session"].add(user)
        await self.request["session"].commit()

        return web.json_response({"status": "success"})

    async def delete(self):
        user_id = int(self.request.match_info["user_id"])
        check_owner(self.request, user_id)
        user = await get_orm_item(User, user_id, self.request["session"])
        await self.request["session"].delete(user)
        await self.request["session"].commit()
        return web.json_response({"status": "success"})


async def app_context(app: web.Application):
    print("START")
    async with engine.begin() as conn:
        async with Session() as session:
            await session.execute('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"')
            await session.commit()
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    print("FINISH")


async def get_app():
    app = web.Application(middlewares=[session_middleware])
    app_auth_required = web.Application(middlewares=[session_middleware, auth_middleware])

    app.cleanup_ctx.append(app_context)
    app.add_routes(
        [
            web.post("/login", login),
            web.post("/users/", UserView),
        ]
    )

    app_auth_required.add_routes(
        [
            web.get("/{user_id:\d+}", UserView),
            web.patch("/{user_id:\d+}", UserView),
            web.delete("/{user_id:\d+}", UserView),
        ]
    )

    app.add_subapp(prefix="/users", subapp=app_auth_required)
    return app
