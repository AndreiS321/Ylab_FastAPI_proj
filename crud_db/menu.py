from typing import List

from sqlalchemy import select, func, update, delete

from app import app
from dataclass import MenuDC
from models import Menu, Submenu, Dish


async def get_menu_db_list() -> List[MenuDC]:
    async with app.database.session_maker() as session:
        stmt = select(Menu)
        answ = (await session.scalars(stmt)).all()
        menus_res = [MenuDC(id=menu.id,
                            title=menu.title,
                            description=menu.description,
                            submenus_count=(await session.scalar(
                                select(func.count(Submenu.id))
                                .select_from(Menu)
                                .join(Submenu, Menu.id == Submenu.menu_id)
                                .group_by(Menu)
                                .having(Menu.id == menu.id))) or 0,
                            dishes_count=(await session.scalar(
                                select(func.count(Dish.id))
                                .select_from(Menu)
                                .join(Dish, Menu.id == Dish.menu_id)
                                .group_by(Menu)
                                .having(Menu.id == menu.id))) or 0)
                     for menu in answ]
    return menus_res


async def get_menu_db(menu_id: int) -> MenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await session.scalar(stmt)
        if not menu:
            return None
        menu_res = MenuDC(id=menu.id,
                          title=menu.title,
                          description=menu.description,
                          submenus_count=(await session.scalar(
                              select(func.count(Submenu.id))
                              .select_from(Menu)
                              .join(Submenu, Menu.id == Submenu.menu_id)
                              .group_by(Menu)
                              .having(Menu.id == menu.id))) or 0,
                          dishes_count=(await session.scalar(
                              select(func.count(Dish.id))
                              .select_from(Menu)
                              .join(Dish, Menu.id == Dish.menu_id)
                              .group_by(Menu)
                              .having(Menu.id == menu.id))) or 0)
    return menu_res


async def create_menu_db(title: str, description: str) -> MenuDC:
    async with app.database.session_maker() as session:
        menu = Menu(title=title, description=description)
        session.add(menu)
        await session.flush()
        menu_res = MenuDC(id=menu.id,
                          title=menu.title,
                          description=menu.description
                          )
        await session.commit()
    return menu_res


async def patch_menu_db(menu_id: int, title: str, description) -> MenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await session.scalar(stmt)
        if not menu:
            return None
        smtm = update(Menu) \
            .where(Menu.id == menu.id) \
            .values(title=title, description=description) \
            .returning(Menu)
        menu_res = await session.scalar(smtm)
        menu_res = MenuDC(id=menu_res.id,
                          title=menu_res.title,
                          description=menu_res.description,
                          submenus_count=(await session.scalar(
                              select(func.count(Submenu.id))
                              .select_from(Menu)
                              .join(Submenu, Menu.id == Submenu.menu_id)
                              .group_by(Menu)
                              .having(Menu.id == menu_res.id))) or 0,
                          dishes_count=(await session.scalar(
                              select(func.count(Dish.id))
                              .select_from(Menu)
                              .join(Dish, Menu.id == Dish.menu_id)
                              .group_by(Menu)
                              .having(Menu.id == menu_res.id))) or 0)
        await session.commit()
    return menu_res


async def delete_menu_db(menu_id: int) -> MenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await session.scalar(stmt)
        if not menu:
            return None
        menu_res = MenuDC(id=menu.id,
                          title=menu.title,
                          description=menu.description,
                          submenus_count=(await session.scalar(
                              select(func.count(Submenu.id))
                              .select_from(Menu)
                              .join(Submenu, Menu.id == Submenu.menu_id)
                              .group_by(Menu)
                              .having(Menu.id == menu.id))) or 0,
                          dishes_count=(await session.scalar(
                              select(func.count(Dish.id))
                              .select_from(Menu)
                              .join(Dish, Menu.id == Dish.menu_id)
                              .group_by(Menu)
                              .having(Menu.id == menu.id))) or 0)
        smtm = delete(Menu) \
            .where(Menu.id == menu.id) \
            .returning(Menu)
        await session.execute(smtm)
        await session.commit()
    return menu_res
