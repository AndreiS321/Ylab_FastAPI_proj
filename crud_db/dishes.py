from sqlalchemy import delete, select, update

from crud_db.utils import (
    BaseAccessor,
    cache_delete,
    cache_get,
    cache_get_all,
    cache_post,
)
from dataclass import DishDC
from models import Dish


class DishesAccessor(BaseAccessor):

    @cache_get_all(1)
    async def get_list(self, submenu_id: int) -> list[DishDC]:
        stmt = select(Dish).where(Dish.submenu_id == submenu_id)
        answ = (await self._session.scalars(stmt)).all()
        dishes_res = [await Dish.dish_to_dc(dish, self._session) for dish in answ]
        return dishes_res

    @cache_get(1)
    async def get(self, **kwargs) -> DishDC | None:
        stmt = select(Dish).filter_by(**kwargs)
        dish = await self._session.scalar(stmt)
        if not dish:
            return None
        dish_res = await Dish.dish_to_dc(dish, self._session)
        return dish_res

    @cache_post(1)
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
        self._session.add(dish)
        await self._session.flush()
        dish_res = await Dish.dish_to_dc(dish, self._session)
        await self._session.commit()
        return dish_res

    @cache_post(1)
    async def patch(
            self, dish_id: int, title: str, description: str, price: float
    ) -> DishDC | None:
        stmt = select(Dish).where(Dish.id == dish_id)
        submenu = await self._session.scalar(stmt)
        if not submenu:
            return None
        smtm = (
            update(Dish)
            .where(Dish.id == submenu.id)
            .values(title=title, description=description, price=price)
            .returning(Dish)
        )
        dish_res = await self._session.scalar(smtm)
        dish_res = await Dish.dish_to_dc(dish_res, self._session)
        await self._session.commit()
        return dish_res

    @cache_delete
    async def delete(self, dish_id: int) -> DishDC | None:
        stmt = select(Dish).where(Dish.id == dish_id)
        dish = await self._session.scalar(stmt)
        if not dish:
            return None
        dish_res = await Dish.dish_to_dc(dish, self._session)
        smtm = delete(Dish).where(Dish.id == dish.id).returning(Dish)
        await self._session.execute(smtm)
        await self._session.commit()
        return dish_res
