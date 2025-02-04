import datetime

import auth
import crud
import models
import schema
from depenedency import SessionDependency, TokenDependency
from fastapi import FastAPI, HTTPException
from lifespan import lifespan
from pydantic import BaseModel
from sqlalchemy import select

app = FastAPI(title="ToDo", version="0.1", description="Список дел", lifespan=lifespan)


@app.post("/v1/todo/", response_model=schema.CreateTodoResponse)
async def create_todo(
        session: SessionDependency,
        create_todo_request: schema.CreateTodoRequest,
        token: TokenDependency
):
    user_id = token.user.id
    create_todo_dict = create_todo_request.dict()
    create_todo_dict["user_id"] = user_id
    todo = models.Todo(**create_todo_dict)
    await auth.check_access_rights(session, token, todo, write=True, read=False)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.get("/v1/todo/{todo_id}", response_model=schema.GetTodoResponse)
async def get_todo(todo_id: int, session: SessionDependency, token: TokenDependency):
    todo = await crud.get_item(session, models.Todo, todo_id)
    await auth.check_access_rights(session, token, todo, write=False, read=True)
    return todo.dict


@app.patch("/v1/todo/{todo_id}", response_model=schema.UpdateTodoResponse)
async def update_todo(
    update_todo_request: schema.UpdateTodoRequest,
    todo_id: int,
    session: SessionDependency,
    token=TokenDependency
):

    todo = await crud.get_item(session, models.Todo, todo_id)
    if todo.user_id != token.user_id:
        raise HTTPException(403, 'not authorized')
    todo_dict = update_todo_request.dict(exclude_none=True)
    if todo_dict.get("done"):
        todo_dict["end_time"] = datetime.datetime.utcnow()
    for field, value in todo_dict.items():
        setattr(todo, field, value)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.delete("/v1/todo/{todo_id}", response_model=schema.DeleteTodoResponse)
async def delete_todo(todo_id: int, session: SessionDependency):

    await crud.delete_item(session, models.Todo, todo_id)
    return {"status": "success"}


@app.post("/v1/user/", response_model=schema.CreateUserResponse)
async def create_user(
    session: SessionDependency, create_user_request: schema.CreateUserRequests
):

    create_user_dict = create_user_request.dict()
    create_user_dict["password"] = auth.hash_password(create_user_dict["password"])
    user = models.User(**create_user_dict)
    role = await auth.get_default_role(session)
    user.roles = [role]
    await crud.add_item(session, user)
    return user.id_dict


@app.post("/v1/login", response_model=schema.LoginResponse)
async def login(login_request: schema.LoginRequest, session: SessionDependency):
    name = login_request.name
    password = login_request.password
    user_query = select(models.User).where(models.User.name == name)
    user_model = await session.scalar(user_query)
    if user_model is None:
        raise HTTPException(401, "User or password is wrong")
    if not auth.check_password(user_model.password, password):
        raise HTTPException(401, "User or password is wrong")
    token = models.Token(user_id=user_model.id)
    await crud.add_item(session, token)
    return token.dict
