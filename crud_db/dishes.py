from typing import List

from sqlalchemy import select, update, delete

from app import app
from dataclass import DishDC
from models import Dish


async def get_dish_db_list(submenu_id: int) -> List[DishDC]:
    async with app.database.session_maker() as session:
        stmt = select(Dish).where(Dish.submenu_id == submenu_id)
        answ = (await session.scalars(stmt)).all()
        dishes_res = [await Dish.dish_to_dc(dish, session)
                      for dish in answ]
    return dishes_res


async def get_dish_db(dish_id: int) -> DishDC:
    async with app.database.session_maker() as session:
        stmt = select(Dish).where(Dish.id == dish_id)
        dish = await session.scalar(stmt)
        if not dish:
            return None
        dish_res = await Dish.dish_to_dc(dish, session)
    return dish_res


async def create_dish_db(menu_id: int, submenu_id: int,
                         title: str, description: str,
                         price: float) -> DishDC:
    async with app.database.session_maker() as session:
        dish = Dish(menu_id=menu_id,
                    submenu_id=submenu_id,
                    title=title,
                    description=description,
                    price=price,
                    )
        session.add(dish)
        await session.flush()
        dish_res = await Dish.dish_to_dc(dish, session)
        await session.commit()
    return dish_res


async def patch_dish_db(dish_id: int, title: str, description: str, price: float) -> DishDC:
    async with app.database.session_maker() as session:
        stmt = select(Dish).where(Dish.id == dish_id)
        submenu = await session.scalar(stmt)
        if not submenu:
            return None
        smtm = update(Dish) \
            .where(Dish.id == submenu.id) \
            .values(title=title, description=description, price=price) \
            .returning(Dish)
        dish_res = await session.scalar(smtm)
        dish_res = await Dish.dish_to_dc(dish_res, session)
        await session.commit()
    return dish_res


async def delete_dish_db(dish_id: int) -> DishDC:
    async with app.database.session_maker() as session:
        stmt = select(Dish).where(Dish.id == dish_id)
        dish = await session.scalar(stmt)
        if not dish:
            return None
        dish_res = await Dish.dish_to_dc(dish, session)
        smtm = delete(Dish) \
            .where(Dish.id == dish.id) \
            .returning(Dish)
        await session.execute(smtm)
        await session.commit()
    return dish_res
