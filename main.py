import os

from dotenv import load_dotenv

from crud import menu, submenu, dishes
from db import Database
from sqlalchemy_base import db
from app import app, FastAPI


def include_routers(app):
    app.include_router(menu.router)
    app.include_router(submenu.router)
    app.include_router(dishes.router)


def start_app(app: "FastAPI"):
    dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    database = Database(app=app)
    app.database = database
    database.connect(db=db)

    include_routers(app)


start_app(app)


@app.get("/")
async def index():
    return {"hello": os.getenv("db_name")}
