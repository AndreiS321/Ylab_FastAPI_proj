# mypy: ignore-errors
import os
from typing import TYPE_CHECKING, AsyncGenerator

import aioredis
from aioredis import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from main import FastAPI

from app import app


class Database:
    def __init__(self, app: 'FastAPI'):
        self.app: 'FastAPI' = app
        self.engine: AsyncEngine | None = None
        self.session_maker: async_sessionmaker | None = None
        self.db: DeclarativeBase | None = None

    def connect(
            self, db: DeclarativeBase, is_test: bool = False, *_: list, **__: dict
    ) -> None:
        self.db = db
        if is_test:
            db_user: str | None = os.getenv('POSTGRES_USER_TEST', default='postgres')
            db_password: str | None = os.getenv('POSTGRES_PASSWORD_TEST', default='postgres')
            db_host: str | None = os.getenv('POSTGRES_HOST_TEST', default='test_database')
            db_port: str | None = os.getenv('POSTGRES_PORT_TEST', default=4321)
            db_name: str | None = os.getenv('POSTGRES_DB_TEST', default='postgres')
        else:
            db_user: str | None = os.getenv('POSTGRES_USER', default='postgres')
            db_password: str | None = os.getenv('POSTGRES_PASSWORD', default='postgres')
            db_host: str | None = os.getenv('POSTGRES_HOST', default='database')
            db_port: str | None = os.getenv('POSTGRES_PORT', default=5432)
            db_name: str | None = os.getenv('POSTGRES_DB', default='postgres')

        self.engine = create_async_engine(
            f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
        )
        self.session_maker = async_sessionmaker(self.engine, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with app.database.session_maker() as session:
        yield session


def init_redis(app: 'FastAPI'):
    host = os.environ.get('REDIS_HOST', 'localhost')
    redis = aioredis.from_url(f'redis://{host}')
    app.redis = redis


async def get_redis_conn() -> AsyncGenerator[Redis, None]:
    async with app.redis.client() as conn:
        yield conn
