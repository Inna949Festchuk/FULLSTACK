import os
import datetime

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase 
from sqlalchemy.orm import mapped_column, Mapped 
from sqlalchemy import DateTime, Integer, String, func 


load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
engine = create_async_engine(PG_DSN)
Session = async_sessionmaker(bind=engine, expire_on_commit=False) 


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Press(Base):
    
    __tablename__ = "app_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(25), nullable=False, unique=True)
    body: Mapped[str] = mapped_column(String(1000), nullable=False)
    registration_time: Mapped[datetime.datetime] =  mapped_column(DateTime, server_default=func.now())
    onwer: Mapped[str] = mapped_column(String(72), nullable=False)
    
    @property 
    def dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'registration_time': self.registration_time.timestamp(),
            'onwer': self.onwer            
        }

    @property
    def dict_id(self):
        return {
            "id": self.id
        }


async def init_orm():
    async with engine.begin() as connect:
        await connect.run_sync(Base.metadata.drop_all)     
        await connect.run_sync(Base.metadata.create_all)

async def close_orm():
    await engine.dispose()