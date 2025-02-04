import datetime
import os
from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import Integer, String, DateTime, ForeignKey,  func, text


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB",)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase, AsyncAttrs):
    pass

class User(Base):

    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(72), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(String(72), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'registration_time': self.registration_time.isoformat()
        }

    @property
    def dict_id(self):
        return {
            "id": self.id
        }

class Advertisement(Base):
    __tablename__ = "advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("app_users.id"), nullable=False)

    @property
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'creation_time': self.creation_time.isoformat(),
            'owner_id': self.owner_id
        }

    @property
    def dict_id(self):
        return {
            "id": self.id
        }

class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, server_default=func.uuid_generate_v4())
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("app_users.id"))
    creation_time: Mapped[datetime.datetime] = mapped_column(DateTime, server_default=func.now())

async def init_orm():
    async with engine.begin() as conn:
        async with Session() as session:
            await session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
            await session.commit()
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()