from typing import Optional, TYPE_CHECKING

from fastapi import FastAPI as FastAPIApp
if TYPE_CHECKING:
    from db import Database


class FastAPI(FastAPIApp):
    database: Optional["Database"] = None


app = FastAPI()
