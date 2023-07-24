from typing import List

from sqlalchemy import func, select, update, delete

from app import app
from dataclass import SubmenuDC
from models import Submenu, Dish


async def get_submenu_db_list(menu_id: int) -> List[SubmenuDC]:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.menu_id == menu_id)
        answ = (await session.scalars(stmt)).all()
        submenus_res = [SubmenuDC(id=submenu.id,
                                  menu_id=submenu.menu_id,
                                  title=submenu.title,
                                  description=submenu.description,
                                  dishes_count=(await session.scalar(
                                      select(func.count(Dish.id))
                                      .select_from(Submenu)
                                      .join(Dish, Submenu.id == Dish.submenu_id)
                                      .group_by(Submenu)
                                      .having(Submenu.id == submenu.id))) or 0)
                        for submenu in answ]
    return submenus_res


async def get_submenu_db(submenu_id: int) -> SubmenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = SubmenuDC(id=submenu.id,
                                menu_id=submenu.menu_id,
                                title=submenu.title,
                                description=submenu.description,
                                dishes_count=(await session.scalar(
                                    select(func.count(Dish.id))
                                    .select_from(Submenu)
                                    .join(Dish, Submenu.id == Dish.submenu_id)
                                    .group_by(Submenu)
                                    .having(Submenu.id == submenu.id))) or 0)
    return submenu_res


async def create_submenu_db(menu_id: int, title: str, description: str) -> SubmenuDC:
    async with app.database.session_maker() as session:
        submenu = Submenu(menu_id=menu_id, title=title, description=description)
        session.add(submenu)
        await session.flush()
        submenu_res = SubmenuDC(id=submenu.id,
                                menu_id=submenu.menu_id,
                                title=submenu.title,
                                description=submenu.description
                                )
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
        submenu_res = SubmenuDC(id=submenu_res.id,
                                menu_id=submenu_res.menu_id,
                                title=submenu_res.title,
                                description=submenu_res.description,
                                dishes_count=(await session.scalar(
                                    select(func.count(Dish.id))
                                    .select_from(Submenu)
                                    .join(Dish, Submenu.id == Dish.submenu_id)
                                    .group_by(Submenu)
                                    .having(Submenu.id == submenu_res.id))) or 0)
        await session.commit()
    return submenu_res


async def delete_submenu_db(submenu_id: int) -> SubmenuDC:
    async with app.database.session_maker() as session:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = SubmenuDC(id=submenu.id,
                                menu_id=submenu.menu_id,
                                title=submenu.title,
                                description=submenu.description,
                                dishes_count=(await session.scalar(
                                    select(func.count(Dish.id))
                                    .select_from(Submenu)
                                    .join(Dish, Submenu.id == Dish.submenu_id)
                                    .group_by(Submenu)
                                    .having(Submenu.id == submenu.id))) or 0)
        smtm = delete(Submenu) \
            .where(Submenu.id == submenu.id) \
            .returning(Submenu)
        await session.execute(smtm)
        await session.commit()
    return submenu_res
