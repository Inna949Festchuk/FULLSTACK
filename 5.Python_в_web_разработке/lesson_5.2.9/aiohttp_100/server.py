import json

from aiohttp import web
from bcrypt import checkpw, gensalt, hashpw
from sqlalchemy.exc import IntegrityError

from models import Session, User, close_orm, init_orm

app = web.Application()


def hash_password(password: str) -> str:
    password_bytes = password.encode()
    hashed_password_bytes = hashpw(password_bytes, gensalt())
    hashed_password = hashed_password_bytes.decode()
    return hashed_password


def check_password(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode()
    hashed_password_bytes = hashed_password.encode()
    return checkpw(password_bytes, hashed_password_bytes)


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    await close_orm()
    print("FINISH")


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        result = await handler(request)
        return result


app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_http_error(error_cls, message):
    message = {"error": message}
    message = json.dumps(message)
    error = error_cls(text=message, content_type="application/json")
    raise error


async def get_user_by_id(user_id: int, session: Session) -> User:
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, "user not found")
    return user


async def delete_user(user: User, session: Session):
    await session.delete(user)
    await session.commit()


async def add_user(user: User, session: Session):
    session.add(user)
    try:
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, "user already exists")


class UserView(web.View):

    @property
    def user_id(self) -> int:
        return int(self.request.match_info["user_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get(self):
        user = await get_user_by_id(self.user_id, self.session)
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        await add_user(user, self.session)
        return web.json_response(user.dict_id)

    async def patch(self):
        user = await get_user_by_id(self.user_id, self.session)
        json_data = await self.request.json()  # {"name": "Anton"}
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        for field, value in json_data.items():
            setattr(user, field, value)
        await add_user(user, self.session)
        return web.json_response(user.dict_id)

    async def delete(self):
        user = await get_user_by_id(self.user_id, self.session)
        await delete_user(user, self.session)
        return web.json_response({"status": "success"})


app.add_routes(
    [
        web.post("/user", UserView),
        web.get("/user/{user_id:\d+}", UserView),
        web.patch("/user/{user_id:\d+}", UserView),
        web.delete("/user/{user_id:\d+}", UserView),
    ]
)

web.run_app(app)
