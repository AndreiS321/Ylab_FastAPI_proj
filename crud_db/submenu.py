from fastapi import Depends
from sqlalchemy import delete, select, update

from dataclass import SubmenuDC
from db import get_session  # type: ignore
from models import Submenu


class SubmenusAccessor:
    def __init__(self, session=Depends(get_session)):
        self.session = session

    async def get_list(self, menu_id: int) -> list[SubmenuDC]:
        stmt = select(Submenu).where(Submenu.menu_id == menu_id)
        answer = (await self.session.scalars(stmt)).all()
        submenus_res = [
            await Submenu.submenu_to_dc(submenu, self.session) for submenu in answer
        ]
        return submenus_res

    async def get(self, **kwargs) -> SubmenuDC | None:
        stmt = select(Submenu).filter_by(**kwargs)
        submenu = await self.session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = await Submenu.submenu_to_dc(submenu, self.session)
        return submenu_res

    async def create(self, menu_id: int, title: str, description: str) -> SubmenuDC:
        submenu = Submenu(menu_id=menu_id, title=title, description=description)
        self.session.add(submenu)
        await self.session.flush()
        submenu_res = await Submenu.submenu_to_dc(submenu, self.session)
        await self.session.commit()
        return submenu_res

    async def patch(
        self, submenu_id: int, title: str, description: str
    ) -> SubmenuDC | None:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await self.session.scalar(stmt)
        if not submenu:
            return None
        smtm = (
            update(Submenu)
            .where(Submenu.id == submenu.id)
            .values(title=title, description=description)
            .returning(Submenu)
        )
        submenu_res = await self.session.scalar(smtm)
        submenu_res = await Submenu.submenu_to_dc(submenu_res, self.session)
        await self.session.commit()
        return submenu_res

    async def delete(self, submenu_id: int) -> SubmenuDC | None:
        stmt = select(Submenu).where(Submenu.id == submenu_id)
        submenu = await self.session.scalar(stmt)
        if not submenu:
            return None
        submenu_res = await Submenu.submenu_to_dc(submenu, self.session)
        smtm = delete(Submenu).where(Submenu.id == submenu.id).returning(Submenu)
        await self.session.execute(smtm)
        await self.session.commit()
        return submenu_res
