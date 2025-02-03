import os
import datetime

# Устанавливаем pip install sqlalchemy и pip install asyncpg
from sqlalchemy.ext.asyncio import (
    AsyncAttrs, # асинхронные атрибуты базового класса Base()
    async_sessionmaker, # асинхронная фабрика сессий
    create_async_engine # асинхронная фабрика подключений к БД
    )

from sqlalchemy.orm import DeclarativeBase # Материнский класс для наследования от него 
                                        # базового класса для создания ORM-моделей
from sqlalchemy.orm import mapped_column, Mapped # колонки и типизация
from sqlalchemy import DateTime, Integer, String, func # типы данных

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# Передаем SQLAlchemy данные для подключения с помощью специальной DSN-строки
PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

# Создаем АСИНХРОННОЕ подключение, передав фабрике подключений DSN-строку 
engine = create_async_engine(PG_DSN)

# Создаем АСИНХРОННЫЙ класс сессий, которые будут использовать подключение async_engine 
Session = async_sessionmaker(bind=engine, expire_on_commit=False) 

# Создаем базовый класс, с методами применимыми ко всем моделям
class Base(DeclarativeBase, AsyncAttrs):
    pass

# Создаем отдельные модели, наследуясь от базового класса Base
class User(Base):
    
    # сопоставляем модель с таблицей в которой будут храниться данные
    __tablename__ = "app_users"

    # теперь задаем поля сапостовляя питоновский тип и постгрессовский
    # задаем PK
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    # Задаем имя, отключив пустые значения index=True, 
    # задав уникальные unique=True (уникальные индексы), с быстрым поиском по имени - индексируем
    name: Mapped[str] = mapped_column(String(72), nullable=False, unique=True)
    # Задаем пароль (говорят что матчится на String)
    password: Mapped[str] = mapped_column(String(72), nullable=False)
    # Время регистрации (матчится на datetime.datetime) 
    # с заданием времени добавления пользователя считываемого с сервера default=datetime.datetime.utcnow
    # с заданием времени добавления пользователя считываемого с базы данных server_default=func.now() Лучший вариант
    registration_time: Mapped[datetime.datetime] =  mapped_column(DateTime, server_default=func.now())

# Инициализируем DB ORM
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