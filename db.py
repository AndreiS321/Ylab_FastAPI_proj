import os
from typing import Optional, TYPE_CHECKING

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from main import FastAPI


class Database:
    def __init__(self, app: "FastAPI"):
        self.app: "FastAPI" = app
        self._engine: Optional[AsyncEngine] = None
        self.session_maker: Optional[async_sessionmaker] = None
        self._db: Optional[DeclarativeBase] = None

    def connect(self, db: DeclarativeBase, *_: list, **__: dict) -> None:
        self._db = db

        db_user = os.getenv("db_user")
        db_password = os.getenv("db_password")
        db_host = os.getenv("db_host")
        db_name = os.getenv("db_name")

        self._engine = create_async_engine(f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}/{db_name}")
        self.session_maker = async_sessionmaker(self._engine)
