import os

from celery import Celery
from sqlalchemy import create_engine, delete
from sqlalchemy.dialects.postgresql import insert

from admin.dataclasses import ExcelMenu
from admin.parsers import parse_excel
from config import load_environment_variables
from models import Dish, Menu, Submenu

load_environment_variables()
broker_user = os.getenv('RABBIT_USER', default='guest')
broker_password = os.getenv('RABBIT_PASSWORD', default='')
broker_host = os.getenv('RABBIT_HOST', default='localhost')
broker_port = os.getenv('RABBIT_PORT', default=5672)
app = Celery('tasks', broker=f'pyamqp://{broker_user}:{broker_password}@{broker_host}:{broker_port}//')


@app.on_after_configure.connect
def setup_celery_excel_task(sender, **kwargs):
    sender.add_periodic_task(15, get_data.s())


@app.task
def write_data_to_db(menus: list[dict]):
    """Принимает список ExcelMenu (в json)"""
    excel_menus: list[ExcelMenu] = [ExcelMenu(**menu) for menu in menus]
    db_user: str | None = os.getenv('POSTGRES_USER', default='postgres')
    db_password: str | None = os.getenv('POSTGRES_PASSWORD', default='postgres')
    db_host: str | None = os.getenv('POSTGRES_HOST', default='database')
    db_port: int | str | None = os.getenv('POSTGRES_PORT', default=5432)
    db_name: str | None = os.getenv('POSTGRES_DB', default='postgres')

    engine = create_engine(
        f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    with engine.begin() as conn:
        for menu in excel_menus:
            # Обновление данных меню из таблицы
            stmt = insert(Menu).values(title=menu.title, description=menu.description)
            resp = conn.execute(
                stmt.on_conflict_do_update(
                    constraint='unique_constraint_menu',
                    set_={
                        'title': stmt.excluded.title,
                        'description': stmt.excluded.description,
                    },
                ).returning(Menu.id)
            )
            menu.id = resp.one()[0]
            for submenu in menu.submenus:
                # Обновление данных подменю из таблицы
                stmt = insert(Submenu).values(
                    title=submenu.title,
                    description=submenu.description,
                    menu_id=menu.id,
                )
                resp = conn.execute(
                    stmt.on_conflict_do_update(
                        constraint='unique_constraint_submenu',
                        set_={
                            'title': stmt.excluded.title,
                            'description': stmt.excluded.description,
                        },
                    ).returning(Submenu.id)
                )
                submenu.id = resp.one()[0]
                for dish in submenu.dishes:
                    # Обновление данных блюд из таблицы
                    stmt = insert(Dish).values(
                        title=dish.title,
                        description=dish.description,
                        price=dish.price,
                        menu_id=menu.id,
                        submenu_id=submenu.id,
                    )
                    resp = conn.execute(
                        stmt.on_conflict_do_update(
                            constraint='unique_constraint_dish',
                            set_={
                                'title': stmt.excluded.title,
                                'description': stmt.excluded.description,
                                'price': stmt.excluded.price,
                            },
                        ).returning(Dish.id)
                    )
                    dish.id = resp.one()[0]

                # Удаление блюд которых нет в таблице
                dish_ids = [dish.id for dish in submenu.dishes]
                stmt = delete(Dish).where(
                    Dish.id.notin_(dish_ids), Dish.submenu_id == submenu.id
                )
                conn.execute(stmt)

            # Удаление подменю которых нет в таблице
            submenu_ids = [submenu.id for submenu in menu.submenus]
            stmt = delete(Submenu).where(
                Submenu.id.notin_(submenu_ids), Submenu.menu_id == menu.id
            )
            conn.execute(stmt)

        # Удаление меню которых нет в таблице
        menu_ids = [menu.id for menu in excel_menus]
        stmt = delete(Menu).where(Menu.id.notin_(menu_ids))
        conn.execute(stmt)


@app.task
def get_data():
    google_mode = os.getenv('GOOGLE_MODE')
    google_mode = (
        bool(int(google_mode))
        if isinstance(google_mode, str) and google_mode.isdigit()
        else google_mode
    )
    if google_mode:
        pass
    else:
        excel_file = os.getenv('EXCEL_FILE')
        parsed_data_dict = parse_excel(file=excel_file)
        write_data_to_db.delay(parsed_data_dict)
