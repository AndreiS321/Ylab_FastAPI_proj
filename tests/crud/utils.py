from sqlalchemy.ext.asyncio import AsyncSession

from crud.pydantic_models import DishOut, MenuOut, SubmenuOut
from models import Dish, Menu, Submenu


async def create_menu(
    menu, session: AsyncSession, with_count=True, convert_types=True
) -> MenuOut:
    menu = Menu(title=menu['title'], description=menu['description'])
    session.add(menu)
    await session.flush()
    menu = await menu.to_pydantic_model(session, with_count=with_count)
    if convert_types:
        menu.id = int(menu.id)
    await session.commit()

    return menu


async def create_submenu(
    submenu, menu_id: int, session: AsyncSession, with_count=True, convert_types=True
) -> SubmenuOut:
    submenu = Submenu(
        title=submenu['title'], description=submenu['description'], menu_id=menu_id
    )
    session.add(submenu)
    await session.flush()
    submenu = await submenu.to_pydantic_model(session, with_count=with_count)
    if convert_types:
        submenu.id = int(submenu.id)
    await session.commit()
    return submenu


async def create_dish(
    dish, menu_id: int, submenu_id: int, session: AsyncSession, convert_types=True
) -> DishOut:
    dish = Dish(
        title=dish['title'],
        description=dish['description'],
        menu_id=menu_id,
        submenu_id=submenu_id,
        price=float(dish['price']),
    )
    session.add(dish)
    await session.flush()
    dish = await dish.to_pydantic_model(session)
    if convert_types:
        dish.id = int(dish.id)
        dish.price = float(dish.price)
    await session.commit()
    return dish
