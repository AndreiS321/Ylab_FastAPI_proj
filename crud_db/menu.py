from typing import List

from fastapi import Depends
from sqlalchemy import select, update, delete

from dataclass import MenuDC
from db import get_session
from models import Menu


class MenusAccessor:
    def __init__(self, session=Depends(get_session)):
        self.session = session

    async def get_list(self) -> List[MenuDC]:
        stmt = select(Menu)
        answ = (await self.session.scalars(stmt)).all()
        menus_res = [await Menu.menu_to_dc(menu, self.session) for menu in answ]
        return menus_res

    async def get(self, **kwargs) -> MenuDC | None:
        stmt = select(Menu).filter_by(**kwargs)
        menu = await self.session.scalar(stmt)

        if not menu:
            return None
        menu_res = await Menu.menu_to_dc(menu, self.session)
        return menu_res

    async def create(self, title: str, description: str) -> MenuDC:
        menu = Menu(title=title, description=description)
        self.session.add(menu)
        await self.session.flush()
        menu_res = MenuDC(id=menu.id, title=menu.title, description=menu.description)
        await self.session.commit()
        return menu_res

    async def patch(self, menu_id: int, title: str, description) -> MenuDC | None:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await self.session.scalar(stmt)
        if not menu:
            return None
        smtm = (
            update(Menu)
            .where(Menu.id == menu.id)
            .values(title=title, description=description)
            .returning(Menu)
        )
        menu_res = await self.session.scalar(smtm)
        menu_res = await Menu.menu_to_dc(menu_res, self.session)
        await self.session.commit()
        return menu_res

    async def delete(self, menu_id: int) -> MenuDC | None:
        stmt = select(Menu).where(Menu.id == menu_id)
        menu = await self.session.scalar(stmt)
        if not menu:
            return None
        menu_res = await Menu.menu_to_dc(menu, self.session)
        smtm = delete(Menu).where(Menu.id == menu.id).returning(Menu)
        await self.session.execute(smtm)
        await self.session.commit()
        return menu_res
