import os
from typing import Optional, TYPE_CHECKING, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncEngine,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from main import FastAPI
from app import app


class Database:
    def __init__(self, app: "FastAPI"):
        self.app: "FastAPI" = app
        self.engine: Optional[AsyncEngine] = None
        self.session_maker: Optional[async_sessionmaker] = None
        self.db: Optional[DeclarativeBase] = None

    def connect(
        self, db: DeclarativeBase, is_test: bool = False, *_: list, **__: dict
    ) -> None:
        self.db = db
        if is_test:
            db_user = os.getenv("POSTGRES_USER_TEST", default="postgres")
            db_password = os.getenv("POSTGRES_PASSWORD_TEST", default="postgres")
            db_host = os.getenv("POSTGRES_HOST_TEST", default="test_database")
            db_port = os.getenv("POSTGRES_PORT_TEST", default=4321)
            db_name = os.getenv("POSTGRES_DB_TEST", default="postgres")
        else:
            db_user = os.getenv("POSTGRES_USER")
            db_password = os.getenv("POSTGRES_PASSWORD")
            db_host = os.getenv("POSTGRES_HOST")
            db_port = os.getenv("POSTGRES_PORT")
            db_name = os.getenv("POSTGRES_DB")

        self.engine = create_async_engine(
            f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )
        self.session_maker = async_sessionmaker(self.engine, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with app.database.session_maker() as session:
        yield session
