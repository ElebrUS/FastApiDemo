import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = f'postgresql+asyncpg://{os.getenv("POSTGRES_USER")}' \
                          f':{os.getenv("POSTGRES_PASSWORD")}' \
                          f'@{os.getenv("POSTGRES_HOST")}' \
                          f':{os.getenv("POSTGRES_PORT", 5432)}' \
                          f'/{os.getenv("POSTGRES_DB")}'

engine = create_async_engine(SQLALCHEMY_DATABASE_URL,  future=True)

Base = declarative_base()


async def get_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False,
                                 class_=AsyncSession)

    return async_session()
