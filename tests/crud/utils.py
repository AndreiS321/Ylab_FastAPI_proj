from sqlalchemy.ext.asyncio import AsyncSession

from dataclass import DishDC, SubmenuDC, MenuDC
from models import Menu, Submenu, Dish


async def create_menu(menu, session: AsyncSession) -> MenuDC:
    menu = Menu(title=menu["title"], description=menu["description"])
    session.add(menu)
    await session.flush()
    menu = await menu.menu_to_dc(menu, session)
    await session.commit()

    return menu


async def create_submenu(submenu, menu_id: int, session: AsyncSession) -> SubmenuDC:
    submenu = Submenu(title=submenu["title"], description=submenu["description"], menu_id=menu_id)
    session.add(submenu)
    await session.flush()
    submenu = await submenu.submenu_to_dc(submenu, session)
    await session.commit()
    return submenu


async def create_dish(dish, menu_id: int, submenu_id: int, session: AsyncSession) -> DishDC:
    dish = Dish(title=dish["title"], description=dish["description"], menu_id=menu_id, submenu_id=submenu_id,
                price=float(dish["price"]))
    session.add(dish)
    await session.flush()
    dish = await dish.dish_to_dc(dish, session)
    await session.commit()
    return dish
