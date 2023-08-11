from sqlalchemy import delete, select, update

from crud.pydantic_models import SubmenuOut
from crud_db.base import BaseAccessor
from crud_db.cache import cache_delete, cache_get, cache_get_all, cache_post
from models import Submenu


class SubmenusAccessor(BaseAccessor):
    pydantic_model = SubmenuOut

    @cache_get_all(1)
    async def get_list(self, menu_id: int) -> list[SubmenuOut]:
        stmt = select(Submenu).where(Submenu.menu_id == menu_id)
        answer = (await self._session.scalars(stmt)).all()
        submenus_res = [
            await submenu.to_pydantic_model(self._session) for submenu in answer
        ]
        return submenus_res

    @cache_get(1)
    async def get(self, menu_id: int, submenu_id: int) -> SubmenuOut | None:
        stmt = select(Submenu).filter_by(id=submenu_id)
        submenu = await self._session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = await submenu.to_pydantic_model(self._session)
        return submenu_res

    @cache_post(1)
    async def create(self, title: str, description: str, menu_id: int) -> SubmenuOut:
        submenu = Submenu(menu_id=menu_id, title=title, description=description)
        self._session.add(submenu)
        await self._session.flush()
        submenu_res = await submenu.to_pydantic_model(self._session)
        await self._session.commit()
        return submenu_res

    @cache_post(1)
    async def patch(
        self, title: str, description: str, menu_id: int, submenu_id: int
    ) -> SubmenuOut | None:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await self._session.scalar(stmt)
        if not submenu:
            return None
        smtm = (
            update(Submenu)
            .where(Submenu.id == submenu.id)
            .values(title=title, description=description)
            .returning(Submenu)
        )
        submenu_res = await self._session.scalar(smtm)
        submenu_res = await submenu_res.to_pydantic_model(self._session)
        await self._session.commit()
        return submenu_res

    @cache_delete
    async def delete(self, menu_id: int, submenu_id: int) -> SubmenuOut | None:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await self._session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = await submenu.to_pydantic_model(self._session)
        smtm = delete(Submenu).where(Submenu.id == submenu.id).returning(Submenu)
        await self._session.execute(smtm)
        await self._session.commit()
        return submenu_res
