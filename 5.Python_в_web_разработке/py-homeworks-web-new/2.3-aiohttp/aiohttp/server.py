import json

from aiohttp import web
from models import init_orm, close_orm, Session, Press
from sqlalchemy.exc import IntegrityError

from shema import CreatPress, UpdatePress # импортируем схемы валидации созданные в  schema.py
from pydantic import ValidationError


app = web.Application()

async def orm_context(app):
    """
    Clean up context manager for sqlalchemy.

    Initialize database in startup event and
    close connection in shutdown event.

    :param app: web.Application
    :yield:
    """
    print("START")
    await init_orm()
    yield
    print("FINISH")
    await close_orm()

@web.middleware 
async def session_middleware(request: web.Request, handler): 
    """
    Middleware for handling database session lifecycle.

    This middleware creates a new database session for each request
    and attaches it to the request object. The session is closed 
    automatically after the request is processed by the handler.

    :param request: web.Request object
    :param handler: The next request handler in the middleware chain
    :return: The result of the handler
    """

    async with Session() as session:
        request.session = session
        result = await handler(request)        
    return result

app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)

def get_http_error(error_cls, message):
    """
    Construct an HTTP error with a JSON body containing the error message.

    :param error_cls: The HTTP error class to raise
    :param message: The error message
    :return: The raised error
    """
    message = {"error": message}
    message = json.dumps(message)
    error = error_cls(text=message, content_type="application/json")
    raise error

async def get_press_by_id(press_id: int, session: Session) -> Press:
    """
    Get the Press object from the database by id.

    :param press_id: The id of the Press object to get
    :param session: The database session
    :return: The Press object
    :raises: HTTPNotFound if the Press object is not found
    """
    press = await session.get(Press, press_id)
    if press is None:
        raise get_http_error(web.HTTPNotFound, "Advert not found")
    return press

async def add_press(press: Press, session: Session):
    """
    Add a Press object to the database.

    :param press: The Press object to add
    :param session: The database session
    :raises: HTTPConflict if the Press object already exists in the database
    """
    session.add(press)
    try: 
        await session.commit()
    except IntegrityError as err:
        raise get_http_error(web.HTTPConflict, "Advert already exists")

async def delete_press(press: Press, session: Session):
    """
    Delete a Press object from the database.

    :param press: The Press object to delete
    :param session: The database session
    """
    await session.delete(press)
    await session.commit()


class PressView(web.View):

    @property
    def press_id(self) -> int:
        return int(self.request.match_info["press_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get(self):
        """
        Get a Press object by id.

        :return: The Press object as JSON
        """
        press = await get_press_by_id(self.press_id, self.session)
        return web.json_response(press.dict)
    
    async def post(self):
        """
        Create a new Press object.

        :param json_data: The JSON data to create a Press object from
        :return: The created Press object as JSON with status 201
        :raises: HTTPBadRequest if the JSON data is invalid according to the schema
        """
        json_data = await self.request.json()
        try:
            press_data = CreatPress(**json_data)  # Валидация данных по схеме
            press = Press(**press_data.model_dump())  # Преобразование валидных данных в объект Press
            await add_press(press, self.session)
            return web.json_response(press.dict_id, status=201)
        except ValidationError as err:
            raise get_http_error(web.HTTPBadRequest, str(err))

    async def patch(self):
        """
        Update a Press object by id.

        :param json_data: The JSON data to update a Press object from
        :return: The updated Press object as JSON
        :raises: HTTPBadRequest if the JSON data is invalid according to the schema
        """
    
        press = await get_press_by_id(self.press_id, self.session)
        json_data = await self.request.json()
        try:
            press_data = UpdatePress(**json_data)  # Валидация данных по схеме
            for field, value in press_data.model_dump(exclude_defaults=True).items():  # Обновление только измененных полей exclude_defaults=True
                setattr(press, field, value)
            await add_press(press, self.session)
            return web.json_response(press.dict_id)
        except ValidationError as err:
            raise get_http_error(web.HTTPBadRequest, str(err))

    async def delete(self):
        """
        Delete a Press object by id.

        :return: JSON response with status "success"
        :raises: HTTPNotFound if the Press object is not found
        """

        press = await get_press_by_id(self.press_id, self.session)
        await delete_press(press, self.session)
        return web.json_response({"status": "success"})


app.add_routes([
    web.post("/press", PressView), 
    web.get("/press/{press_id:\d+}", PressView),
    web.patch("/press/{press_id:\d+}", PressView),
    web.delete("/press/{press_id:\d+}", PressView)   
])

web.run_app(app)