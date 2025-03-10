import datetime
import uuid

from config import POSTGRES_DB, POSTGRES_HOST, POSTGRES_PASSWORD, POSTGRES_PORT, POSTGRES_USER, SQL_DEBUG
from custom_types import ModelName
from sqlalchemy import (
    UUID,
    Boolean,
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    String,
    Table,
    UniqueConstraint,
    func,
)
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

engine = create_async_engine(
    f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}",
    echo=SQL_DEBUG,
)

Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


role_rights = Table(
    "role_right_relation",
    Base.metadata,
    Column("role_id", ForeignKey("role.id"), index=True),  # index
    Column("right_id", ForeignKey("right.id"), index=True),
)

user_roles = Table(
    "user_role_relation",
    Base.metadata,
    Column("user_id", ForeignKey("todo_user.id"), index=True),
    Column("role_id", ForeignKey("role.id"), index=True),
)


class Right(Base):
    __tablename__ = "right"
    __table_args__ = (
        CheckConstraint("model in ('user', 'todo', 'token', 'role', 'right')"),
        UniqueConstraint("model", "write", "read", "only_own"),
    )
    _model = "right"

    id: Mapped[int] = mapped_column(primary_key=True)
    write: Mapped[bool] = mapped_column(Boolean, default=False)
    read: Mapped[bool] = mapped_column(Boolean, default=False)
    only_own: Mapped[bool] = mapped_column(Boolean, default=True)
    model: Mapped[ModelName] = mapped_column(String(50), nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "model": self.model,
            "write": self.write,
            "read": self.read,
            "only_own": self.only_own,
        }


class Role(Base):
    __tablename__ = "role"
    _model = "role"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    rights: Mapped[list[Right]] = relationship(
        secondary=role_rights,
        lazy="joined",
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "rights": [right.id for right in self.rights],
        }


class User(Base):
    __tablename__ = "todo_user"
    _model = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )
    password: Mapped[str] = mapped_column(String(70), nullable=False)

    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    tokens: Mapped[list["Token"]] = relationship(
        "Token",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    todos: Mapped[list["Todo"]] = relationship(
        "Todo",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="joined",
    )
    roles: Mapped[list[Role]] = relationship(
        secondary=user_roles,
        lazy="joined",
    )

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "todos": [todo.id for todo in self.todos],
        }


class Token(Base):
    __tablename__ = "token"
    _model = "token"

    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID,
        server_default=func.gen_random_uuid(),
        unique=True,
    )
    creation_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped[User] = relationship(
        User,
        back_populates="tokens",
        lazy="joined",
    )

    @property
    def dict(self):
        return {"id": self.id, "token": self.token, "user_id": self.user_id}


class Todo(Base):
    __tablename__ = "todo"
    _model = "todo"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    important: Mapped[bool] = mapped_column(Boolean, default=False)
    done: Mapped[bool] = mapped_column(Boolean, default=False)
    start_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )
    finish_time: Mapped[datetime.datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("todo_user.id"))
    user: Mapped[User] = relationship(User, back_populates="todos")

    @property
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "important": self.important,
            "done": self.done,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "finish_time": self.finish_time.isoformat() if self.finish_time else None,
            "user_id": self.user_id,
        }


MODEL = User | Token | Todo | Role | Right
MODEL_CLS = type[MODEL]
