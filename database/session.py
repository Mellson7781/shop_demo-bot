from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os


#Выгрузка из .env
load_dotenv
DB_URL = os.getenv("DB_URL")


#Создание асинхронного двигателя бд
engine = create_async_engine(DB_URL, echo=True)


#Асинхронная сессия
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)