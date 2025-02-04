import datetime
from typing import Literal

from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class Status(BaseModel):
    status: Literal["success"]


class CreateTodoRequest(BaseModel):
    title: str
    description: str
    important: bool = False


class CreateTodoResponse(IdResponse):
    pass


class GetTodoResponse(BaseModel):
    id: int
    title: str
    description: str
    important: bool
    done: bool
    start: datetime.datetime
    end_time: datetime.datetime | None = None


class UpdateTodoRequest(BaseModel):
    title: str | None = None
    description: str | None = None
    important: bool | None = None
    done: bool | None = None


class UpdateTodoResponse(IdResponse):
    pass


class DeleteTodoResponse(Status):
    pass
