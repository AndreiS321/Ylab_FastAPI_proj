from sqlalchemy import delete, select, update

from crud_db.utils import (
    BaseAccessor,
    cache_delete,
    cache_get,
    cache_get_all,
    cache_post,
)
from dataclass import MenuDC
from models import Menu


class MenusAccessor(BaseAccessor):
    @cache_get_all(1)
    async def get_list(self) -> list[MenuDC]:
        stmt = select(Menu)
        answ = (await self._session.scalars(stmt)).all()
        menus_res = [await Menu.menu_to_dc(menu, self._session) for menu in answ]
        return menus_res

    @cache_get(1)
    async def get(self, **kwargs) -> MenuDC | None:
        stmt = select(Menu).filter_by(**kwargs)
        menu = await self._session.scalar(stmt)
        if not menu:
            return None
        menu_res = await Menu.menu_to_dc(menu, self._session)
        return menu_res

    @cache_post(1)
    async def create(self, title: str, description: str) -> MenuDC:
        menu = Menu(title=title, description=description)
        self._session.add(menu)
        await self._session.flush()
        menu_res = MenuDC(
            id=menu.id,
            title=menu.title,
            description=menu.description,
            submenus_count=0,
            dishes_count=0,
        )
        await self._session.commit()
        return menu_res

    @cache_post(1)
    async def patch(self, menu_id: int, title: str, description) -> MenuDC | None:
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
        menu_res = await Menu.menu_to_dc(menu_res, self._session)
        await self._session.commit()
        return menu_res

    @cache_delete
    async def delete(self, menu_id: int) -> MenuDC | None:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await self._session.scalar(stmt)
        if not menu:
            return None
        menu_res = await Menu.menu_to_dc(menu, self._session)
        smtm = delete(Menu).where(Menu.id == menu.id).returning(Menu)
        await self._session.execute(smtm)
        await self._session.commit()
        return menu_res
