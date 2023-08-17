from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

import config
import db
import sqlalchemy_base
from app import app
from crud import common, dishes, menu, submenu
from db import Database  # type: ignore

base_url = 'http://127.0.0.1:8000'

config.load_environment_variables()
app.database = Database(app)
app.database.connect(db=sqlalchemy_base.db, is_test=True)
db.init_redis(app)
app.include_router(menu.router)
app.include_router(submenu.router)
app.include_router(dishes.router)
app.include_router(common.router)


@pytest.fixture(autouse=True)
async def setup_db():
    async with app.database.engine.begin() as conn:
        await conn.run_sync(sqlalchemy_base.db.metadata.create_all)
    yield
    async with app.database.engine.begin() as conn:
        await conn.run_sync(sqlalchemy_base.db.metadata.drop_all)


@pytest.fixture(autouse=True)
async def setup_redis():
    yield
    await app.redis.flushall()


@pytest.fixture()
async def session() -> AsyncSession:
    async with app.database.session_maker() as session:
        yield session


@pytest.fixture(scope='session')
async def client() -> AsyncClient:
    async with AsyncClient(app=app, base_url=base_url) as client:
        yield client
