import os

# Используем асинхронный движок для работы с БД
from sqlalchemy.ext.asyncio import create_async_engine
# Используем фабрику асинхронных сессий
from sqlalchemy.ext.asyncio import async_sessionmaker
# Используем базовый класс для создания моделей
from sqlalchemy.orm import DeclarativeBase
# Импортируем класс АИНХРОННЫЕ АТРИБУТЫ
from sqlalchemy.ext.asyncio import AsyncAttrs

from sqlalchemy.orm import mapped_column, Mapped # колонки и типизация
# Импортируем типы данных
from sqlalchemy import Integer, JSON

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# DSN строка отлична для работы в АСИНХРОННОМ РЕЖИМЕ
PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем асинхронный движок для работы с БД
engine = create_async_engine(PG_DSN)

# Создаем фабрику асинхронных сессий
Session = async_sessionmaker(bind=engine, expire_on_commit=False)
# expire_on_commit=False - отключаем закрытие сессии после первого же коммита

# Создаем базовый класс для создания моделей
class Base(DeclarativeBase, AsyncAttrs):
    # мы хотим чтобы некоторые атрибуты нашей модели
    # стали асинхронными поэтому делаем
    # множественное наследование от класса AsyncAttrs
    pass

# Создаем нашу модель
class SwapiPeople(Base):
    __tablename__ = "swapi_people"

    # Смотрим наши JSON (те которые мы получаем при обращении на сервак)
    # Задаем поля сопоставляя питоновский тип с постгрессовским
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    json: Mapped[dict] = mapped_column(JSON, nullable=True) # nullable=True - обязательное поле

# Запросы к БД будут уходить асинхронно,
# соответственно они должны быть внутри event loop

# Инициализируем ORM
async def init_orm():
    # для этого из engine с помощью менеджера контекста with
    # вырвем одно подключение и в нем с помощью 
    # "запускатора" run.sync() выполним запрос в базу на создание таблиц,
    # которые привязаны к модели, что создаст таблицу "swapi_people"
    async with engine.begin() as connect:
        # Решаем проблему НАСЛОЕНИЯ
        # Удаляем предыдущие записи
        await connect.run_sync(Base.metadata.drop_all)     

        await connect.run_sync(Base.metadata.create_all)

# Функция, закрывающая ORM
async def close_orm():
    await engine.dispose()







