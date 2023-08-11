import config
import db
import sqlalchemy_base
from app import FastAPI, app
from crud import common, dishes, menu, submenu


def include_routers(app: 'FastAPI'):
    app.include_router(menu.router)
    app.include_router(submenu.router)
    app.include_router(dishes.router)
    app.include_router(common.router)


def start_app(app: 'FastAPI'):
    config.load_environment_variables()
    include_routers(app)
    db.init_redis(app)
    app.database = db.Database(app)
    app.database.connect(sqlalchemy_base.db)


start_app(app)


@app.get('/')
async def index():
    return {'hello': 'world'}
