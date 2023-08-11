from sqlalchemy import delete, select, update

from crud.pydantic_models import DishOut
from crud_db.base import BaseAccessor
from crud_db.cache import cache_delete, cache_get, cache_get_all, cache_post
from models import Dish


class DishesAccessor(BaseAccessor):
    pydantic_model = DishOut

    @cache_get_all(1)
    async def get_list(self, menu_id: int, submenu_id: int) -> list[DishOut]:
        stmt = select(Dish).where(Dish.submenu_id == submenu_id)
        answ = (await self._session.scalars(stmt)).all()
        dishes_res = [await dish.to_pydantic_model(self._session) for dish in answ]
        return dishes_res

    @cache_get(1)
    async def get(self, menu_id: int, submenu_id: int, dish_id: int) -> DishOut | None:
        stmt = select(Dish).filter_by(id=dish_id)
        dish = await self._session.scalar(stmt)
        if not dish:
            return None
        dish_res = await dish.to_pydantic_model(self._session)
        return dish_res

    @cache_post(1)
    async def create(
        self,
        title: str,
        description: str,
        price: float,
        menu_id: int,
        submenu_id: int,
    ) -> DishOut:
        dish = Dish(
            menu_id=menu_id,
            submenu_id=submenu_id,
            title=title,
            description=description,
            price=price,
        )
        self._session.add(dish)
        await self._session.flush()
        dish_res = await dish.to_pydantic_model(self._session)
        await self._session.commit()
        return dish_res

    @cache_post(1)
    async def patch(
        self,
        title: str,
        description: str,
        price: float,
        menu_id: int,
        submenu_id: int,
        dish_id: int,
    ) -> DishOut | None:
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
        dish_res = await dish_res.to_pydantic_model(self._session)
        await self._session.commit()
        return dish_res

    @cache_delete
    async def delete(
        self, menu_id: int, submenu_id: int, dish_id: int
    ) -> DishOut | None:
        stmt = select(Dish).where(Dish.id == dish_id)
        dish = await self._session.scalar(stmt)
        if not dish:
            return None
        dish_res = await dish.to_pydantic_model(self._session)
        smtm = delete(Dish).where(Dish.id == dish.id).returning(Dish)
        await self._session.execute(smtm)
        await self._session.commit()
        return dish_res
