from typing import TYPE_CHECKING

from aioredis import Redis
from fastapi import FastAPI as FastAPIApp

if TYPE_CHECKING:
    from db import Database


class FastAPI(FastAPIApp):
    database: 'Database'
    redis: 'Redis'


app = FastAPI()
