import os
import atexit
import datetime

from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import mapped_column, Mapped 
from sqlalchemy import DateTime, Integer, String, func 

POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.getenv("POSTGRES_DB", "test")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

PG_DSN = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@" \
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(PG_DSN)

atexit.register(engine.dispose)

Session = sessionmaker(bind=engine) 

class Base(DeclarativeBase):
    
    @property
    def id_dict(self):
        return {'id': self.id}

class Press(Base):
    __tablename__ = "app_press"
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
            'registration_time': self.registration_time.isoformat(),
            'onwer': self.onwer            
        }

Base.metadata.create_all(bind=engine)
