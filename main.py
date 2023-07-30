import os
import config
from dotenv import load_dotenv

import sqlalchemy_base
from crud import menu, submenu, dishes
import db
from app import app, FastAPI


def include_routers(app):
    app.include_router(menu.router)
    app.include_router(submenu.router)
    app.include_router(dishes.router)


def start_app(app: "FastAPI"):
    include_routers(app)
    app.database = db.Database(app)
    app.database.connect(sqlalchemy_base.db)



start_app(app)


@app.get("/")
async def index():
    return {"hello": os.getenv("db_name")}
