from typing import List

from sqlalchemy import select, update, delete

from app import app
from dataclass import SubmenuDC
from models import Submenu


async def get_submenu_db_list(menu_id: int) -> List[SubmenuDC]:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.menu_id == menu_id)
        answ = (await session.scalars(stmt)).all()
        submenus_res = [await Submenu.submenu_to_dc(submenu, session)
                        for submenu in answ]
    return submenus_res


async def get_submenu_db(submenu_id: int) -> SubmenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = await Submenu.submenu_to_dc(submenu, session)
    return submenu_res


async def create_submenu_db(menu_id: int, title: str, description: str) -> SubmenuDC:
    async with app.database.session_maker() as session:
        submenu = Submenu(menu_id=menu_id, title=title, description=description)
        session.add(submenu)
        await session.flush()
        submenu_res = await Submenu.submenu_to_dc(submenu, session)
        await session.commit()
    return submenu_res


async def patch_submenu_db(submenu_id: int, title: str, description: str) -> SubmenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await session.scalar(stmt)
        if not submenu:
            return None
        smtm = update(Submenu) \
            .where(Submenu.id == submenu.id) \
            .values(title=title, description=description) \
            .returning(Submenu)
        submenu_res = await session.scalar(smtm)
        submenu_res = await Submenu.submenu_to_dc(submenu_res, session)
        await session.commit()
    return submenu_res


async def delete_submenu_db(submenu_id: int) -> SubmenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = await Submenu.submenu_to_dc(submenu, session)
        smtm = delete(Submenu) \
            .where(Submenu.id == submenu.id) \
            .returning(Submenu)
        await session.execute(smtm)
        await session.commit()
    return submenu_res
