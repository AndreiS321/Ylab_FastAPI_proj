from fastapi import Depends
from sqlalchemy import delete, select, update

from dataclass import DishDC
from db import get_session
from models import Dish


class DishesAccessor:
    def __init__(self, session=Depends(get_session)):
        self.session = session

    async def get_list(self, submenu_id: int) -> list[DishDC]:
        stmt = select(Dish).where(Dish.submenu_id == submenu_id)
        answ = (await self.session.scalars(stmt)).all()
        dishes_res = [await Dish.dish_to_dc(dish, self.session) for dish in answ]
        return dishes_res

    async def get(self, **kwargs) -> DishDC | None:
        stmt = select(Dish).filter_by(**kwargs)
        dish = await self.session.scalar(stmt)
        if not dish:
            return None
        dish_res = await Dish.dish_to_dc(dish, self.session)
        return dish_res

    async def create(
        self, menu_id: int, submenu_id: int, title: str, description: str, price: float
    ) -> DishDC:
        dish = Dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            title=title,
            description=description,
            price=price,
        )
        self.session.add(dish)
        await self.session.flush()
        dish_res = await Dish.dish_to_dc(dish, self.session)
        await self.session.commit()
        return dish_res

    async def patch(
        self, dish_id: int, title: str, description: str, price: float
    ) -> DishDC | None:
        stmt = select(Dish).where(Dish.id == dish_id)
        submenu = await self.session.scalar(stmt)
        if not submenu:
            return None
        smtm = (
            update(Dish)
            .where(Dish.id == submenu.id)
            .values(title=title, description=description, price=price)
            .returning(Dish)
        )
        dish_res = await self.session.scalar(smtm)
        dish_res = await Dish.dish_to_dc(dish_res, self.session)
        await self.session.commit()
        return dish_res

    async def delete(self, dish_id: int) -> DishDC | None:
        stmt = select(Dish).where(Dish.id == dish_id)
        dish = await self.session.scalar(stmt)
        if not dish:
            return None
        dish_res = await Dish.dish_to_dc(dish, self.session)
        smtm = delete(Dish).where(Dish.id == dish.id).returning(Dish)
        await self.session.execute(smtm)
        await self.session.commit()
        return dish_res
