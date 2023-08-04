import db
import sqlalchemy_base
from app import app, FastAPI
from crud.routers import router_dishes, router_menus, router_submenus


def include_routers(app: "FastAPI"):
    app.include_router(router_menus)
    app.include_router(router_submenus)
    app.include_router(router_dishes)


def start_app(app: "FastAPI"):
    include_routers(app)
    app.database = db.Database(app)
    app.database.connect(sqlalchemy_base.db)


start_app(app)


@app.get("/")
async def index():
    return {"hello": "world"}
