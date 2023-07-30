import os
from typing import Optional, TYPE_CHECKING

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from sqlalchemy.orm import DeclarativeBase

if TYPE_CHECKING:
    from main import FastAPI


class Database:
    def __init__(self, app: "FastAPI"):
        self.app: "FastAPI" = app
        self.engine: Optional[AsyncEngine] = None
        self.session_maker: Optional[async_sessionmaker] = None
        self.db: Optional[DeclarativeBase] = None

    def connect(self, db: DeclarativeBase, is_test: bool = False, *_: list, **__: dict) -> None:
        self.db = db
        if is_test:
            db_user = os.getenv("db_user_test")
            db_password = os.getenv("db_password_test")
            db_host = os.getenv("db_host_test")
            db_port = os.getenv("db_port_test")
            db_name = os.getenv("db_name_test")
        else:
            db_user = os.getenv("db_user")
            db_password = os.getenv("db_password")
            db_host = os.getenv("db_host")
            db_port = os.getenv("db_port")
            db_name = os.getenv("db_name")

        self.engine = create_async_engine(f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")
        self.session_maker = async_sessionmaker(self.engine, class_=AsyncSession)
