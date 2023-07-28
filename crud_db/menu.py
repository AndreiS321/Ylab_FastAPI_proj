from typing import List

from sqlalchemy import select, update, delete

from app import app
from dataclass import MenuDC
from models import Menu


async def get_menu_db_list() -> List[MenuDC]:
    async with app.database.session_maker() as session:
        stmt = select(Menu)
        answ = (await session.scalars(stmt)).all()
        menus_res = [await Menu.menu_to_dc(menu, session)
                     for menu in answ]
    return menus_res


async def get_menu_db(menu_id: int) -> MenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await session.scalar(stmt)

        if not menu:
            return None
        menu_res = await Menu.menu_to_dc(menu, session)
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
        menu_res = await Menu.menu_to_dc(menu_res, session)
        await session.commit()
    return menu_res


async def delete_menu_db(menu_id: int) -> MenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await session.scalar(stmt)
        if not menu:
            return None
        menu_res = await Menu.menu_to_dc(menu, session)
        smtm = delete(Menu) \
            .where(Menu.id == menu.id) \
            .returning(Menu)
        await session.execute(smtm)
        await session.commit()
    return menu_res
