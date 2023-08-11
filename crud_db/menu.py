from sqlalchemy import delete, select, update

from crud.pydantic_models import MenuOut
from crud_db.base import BaseAccessor
from crud_db.cache import cache_delete, cache_get, cache_get_all, cache_post
from models import Menu


class MenusAccessor(BaseAccessor):
    pydantic_model = MenuOut

    @cache_get_all(1)
    async def get_list(self) -> list[MenuOut]:
        stmt = select(Menu)
        answ = (await self._session.scalars(stmt)).all()
        menus_res = [await menu.to_pydantic_model(self._session) for menu in answ]
        return menus_res

    @cache_get(1)
    async def get(self, menu_id: int) -> MenuOut | None:
        stmt = select(Menu).filter_by(id=menu_id)
        menu = await self._session.scalar(stmt)
        if not menu:
            return None
        menu_res = await menu.to_pydantic_model(self._session)
        return menu_res

    @cache_post(1)
    async def create(self, title: str, description: str) -> MenuOut:
        menu = Menu(title=title, description=description)
        self._session.add(menu)
        await self._session.flush()
        menu_res = await menu.to_pydantic_model(self._session)
        await self._session.commit()
        return menu_res

    @cache_post(1)
    async def patch(self, title: str, description, menu_id: int) -> MenuOut | None:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await self._session.scalar(stmt)
        if not menu:
            return None
        smtm = (
            update(Menu)
            .where(Menu.id == menu.id)
            .values(title=title, description=description)
            .returning(Menu)
        )
        menu_res = await self._session.scalar(smtm)
        menu_res = await menu_res.to_pydantic_model(self._session)
        await self._session.commit()
        return menu_res

    @cache_delete
    async def delete(self, menu_id: int) -> MenuOut | None:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await self._session.scalar(stmt)
        if not menu:
            return None
        menu_res = await menu.to_pydantic_model(self._session)
        smtm = delete(Menu).where(Menu.id == menu.id).returning(Menu)
        await self._session.execute(smtm)
        await self._session.commit()
        return menu_res
