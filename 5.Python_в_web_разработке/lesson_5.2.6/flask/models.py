import os
import atexit
import datetime

from sqlalchemy import create_engine # Фабрика различных подключений к БД
from sqlalchemy.orm import sessionmaker # Фабрика создания сессий
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
# PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@ \
#     {POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
PG_DSN = "postgresql://postgres:admin@127.0.0.1:5432/test"

# Создаем подключение, передав фабрике подключений DSN-строку 
engine = create_engine(PG_DSN)

# Для коректного отключения от БД при завершении работы приложения
# используем метод engine-а dispose
atexit.register(engine.dispose)

# Создаем класс сессий, которые будут использовать подключение engine 
Session = sessionmaker(bind=engine) 

# Создаем базовый класс, с методами применимыми ко всем моделям
class Base(DeclarativeBase):
    
    # Если мы хотим метод который будет пременим ко всем молделям задаем его здесь
    # Мы хотим чтобы все подели возвращали свои ID  в виде словаря
    @property
    def id_dict(self):
        return {'id': self.id}

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
    # с заданием времени добавления пользователя считываемого с базы данных server_default=func.now()
    registration_time: Mapped[datetime.datetime] =  mapped_column(DateTime, server_default=func.now())

    # Опишим то, как мы будем преобразовывать объекты этой модели в словари python
    # это будет нужно в дальнейшем для формирования ответа клиенту в виде байтовой строки JSON - b`{}
    @property # если я хочу вызывать dict не как метод User().dict(), а как свойство User().dict
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'password': self.password,
            # так как формат JSON не понимает питоновского datetime
            # ключу "registration_time" нужно присвоить дату и время в формате ISO-строки
            'registration_time': self.registration_time.isoformat()
            
        }

# Создаем миграции для создания таблиц в базе
Base.metadata.create_all(bind=engine)
