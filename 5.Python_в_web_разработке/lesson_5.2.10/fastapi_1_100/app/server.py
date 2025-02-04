import datetime

import crud
import models
import schema
from depenedency import SessionDependency
from fastapi import FastAPI
from lifespan import lifespan
from pydantic import BaseModel

app = FastAPI(title="ToDo", version="0.1", description="Список дел", lifespan=lifespan)


@app.post("/v1/todo/", response_model=schema.CreateTodoResponse)
async def create_todo(
    session: SessionDependency, create_todo_request: schema.CreateTodoRequest
):
    create_todo_dict = create_todo_request.dict()
    todo = models.Todo(**create_todo_dict)
    await crud.add_item(session, todo)
    return todo.id_dict


@app.get("/v1/todo/{todo_id}", response_model=schema.GetTodoResponse)
async def get_todo(todo_id: int, session: SessionDependency):
    todo = await crud.get_item(session, models.Todo, todo_id)
    return todo.dict


@app.patch("/v1/todo/{todo_id}", response_model=schema.UpdateTodoResponse)
async def update_todo(
    update_todo_request: schema.UpdateTodoRequest,
    todo_id: int,
    session: SessionDependency,
):

    todo = await crud.get_item(session, models.Todo, todo_id)
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
