from os import getenv

from dotenv import load_dotenv
from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()


DB_USER = getenv('DB_USER')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_NAME = getenv('DB_NAME')
DB_PORT = getenv('DB_PORT')

DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
engine = create_async_engine(DATABASE_URL)

metadata = MetaData()
