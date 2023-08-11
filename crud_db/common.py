from sqlalchemy import select

from crud.pydantic_models import MenuOutList, SubmenuOutList
from crud_db.base import BaseAccessor
from models import Dish, Menu, Submenu


class CommonAccessor(BaseAccessor):
    async def get_list(self):
        smtm = (
            select(Menu, Submenu, Dish)
            .select_from(Menu)
            .join(Submenu, Submenu.menu_id == Menu.id, isouter=True)
            .join(
                Dish,
                Dish.menu_id == Menu.id and Dish.submenu_id == Submenu.id,
                isouter=True,
            )
        )
        res = (await self._session.execute(smtm)).all()
        result = []
        menus = {i[0] for i in res}
        submenus = {i[1] for i in res}
        dishes = {i[2] for i in res}
        cur_menu = 0
        cur_submenu = 0
        for menu in menus:
            result.append(
                MenuOutList(
                    menu=await menu.to_pydantic_model(self._session, with_count=False),
                    submenus=[],
                )
            )
            for submenu in submenus:
                if submenu and submenu.menu_id == menu.id:
                    result[cur_menu].submenus.append(
                        SubmenuOutList(
                            submenu=await submenu.to_pydantic_model(
                                self._session, with_count=False
                            ),
                            dishes=[],
                        )
                    )
                    for dish in dishes:
                        if dish and dish.submenu_id == submenu.id:
                            result[cur_menu].submenus[cur_submenu].dishes.append(
                                await dish.to_pydantic_model(self._session)
                            )

                cur_submenu += 1
            cur_menu += 1

        return result
