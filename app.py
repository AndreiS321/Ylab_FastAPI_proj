from typing import TYPE_CHECKING, Optional

from fastapi import FastAPI as FastAPIApp

if TYPE_CHECKING:
    from db import Database


class FastAPI(FastAPIApp):
    database: Optional['Database'] = None


app = FastAPI()
