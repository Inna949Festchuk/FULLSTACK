import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import Integer, String

# Переменные окружения для подключения к базе данных
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# DSN строка для работы с базой данных
PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
          f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем асинхронный движок для работы с БД
engine = create_async_engine(PG_DSN)

# Создаем фабрику асинхронных сессий
Session = async_sessionmaker(bind=engine, expire_on_commit=False)

# Создаем базовый класс для создания моделей
class Base(DeclarativeBase, AsyncAttrs):
    pass

# Создаем нашу модель
class SwapiPeople(Base):
    __tablename__ = "home_task_swapi"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String, nullable=True)
    eye_color: Mapped[str] = mapped_column(String, nullable=True)
    films: Mapped[str] = mapped_column(String, nullable=True)
    gender: Mapped[str] = mapped_column(String, nullable=True)
    hair_color: Mapped[str] = mapped_column(String, nullable=True)
    height: Mapped[str] = mapped_column(String, nullable=True)
    homeworld: Mapped[str] = mapped_column(String, nullable=True)
    mass: Mapped[str] = mapped_column(String, nullable=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    skin_color: Mapped[str] = mapped_column(String, nullable=True)
    species: Mapped[str] = mapped_column(String, nullable=True)
    starships: Mapped[str] = mapped_column(String, nullable=True)
    vehicles: Mapped[str] = mapped_column(String, nullable=True)

# Инициализируем ORM
async def init_orm():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)
        await connect.run_sync(Base.metadata.create_all)

# Функция, закрывающая ORM
async def close_orm():
    await engine.dispose()
