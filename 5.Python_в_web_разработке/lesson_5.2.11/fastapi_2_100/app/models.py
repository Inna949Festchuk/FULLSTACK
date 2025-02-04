import datetime
import uuid

from config import PG_DSN
from sqlalchemy import Boolean, DateTime, Integer, String, UUID, ForeignKey, func, Column, UniqueConstraint, CheckConstraint, Table
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from data_types import FieldStr

engine = create_async_engine(
    PG_DSN,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)



class Base(AsyncAttrs, DeclarativeBase):

    @property
    def id_dict(self):
        return {"id": self.id}


role_rights = Table(
    "role_rights_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),
    Column("right_id", ForeignKey("right.id"), index=True)
)


user_roles = Table(
    "user_roles_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),
    Column("user_id", ForeignKey("todo_user.id"), index=True)
)


class Right(Base):
    __tablename__ = "right"
    _model = "right"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=True)
    model: Mapped[FieldStr] = mapped_column(String, nullable=True)

    __table_args__ = (
        UniqueConstraint("model", "only_own", "read", "write"),
        CheckConstraint("model in ('user', 'todo', 'token', 'right', 'role')")
    )

class Role(Base):
    __tablename__ = "role"
    _model = "role"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    rights: Mapped[list[Right]] = relationship(secondary=role_rights)

class Todo(Base):
    __tablename__ = "todo"
    _model = "todo"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime, nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped["User"] = relationship("User", lazy="joined", back_populates="todos")

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
            "user_id": self.user_id
        }


class User(Base):
    __tablename__ = "todo_user"
    _model = "user"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    tokens: Mapped[list["Token"]] = relationship("Token", lazy="joined", back_populates="user")
    todos: Mapped[list["Todo"]] = relationship("Todo", lazy="joined", back_populates="user")
    roles: Mapped[list[Role]] = relationship(Role, secondary=user_roles, lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "roles": [role.id for role in self.roles],
            "todos": [todo.id for todo in self.todos]
        }

class Token(Base):
    __tablename__ = "token"
    _model = "token"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, server_default=func.gen_random_uuid(), unique=True
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped[User] = relationship(User, lazy="joined", back_populates="tokens")


    @property
    def dict(self):
        return {
            "token": self.token
        }


ORM_OBJECT = Todo | User | Token | Role | Right
ORM_CLS = type[Todo] | type[User] | type[Token] | type[Role] | type[Right]
