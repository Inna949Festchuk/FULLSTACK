import datetime

from config import PG_DSN
from sqlalchemy import Boolean, DateTime, Integer, String, func
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine(
    PG_DSN,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


class Todo(Base):
    __tablename__ = "todo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)

    @property
    def dict(self):
        if self.end_time is None:
            end_time = None
        else:
            end_time = self.end_time.isoformat()
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "important": self.important,
            "done": self.done,
            "start": self.start_time.isoformat(),
            "end_time": end_time,
        }


ORM_OBJECT = Todo
ORM_CLS = type[Todo]
