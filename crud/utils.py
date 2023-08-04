from crud.pydantic_models import (
    DishOut,
    SubmenuOut,
    SubmenuOutWithoutCount,
    MenuOut,
    MenuOutWithoutCount,
)
from dataclass import DishDC, SubmenuDC, MenuDC


def menuDC_to_pydantic_menu_out(
    menu: MenuDC, without_count: bool = False
) -> MenuOut | MenuOutWithoutCount:
    if without_count:
        return MenuOutWithoutCount(
            id=str(menu.id), title=menu.title, description=menu.description
        )
    return MenuOut(
        id=str(menu.id),
        title=menu.title,
        description=menu.description,
        submenus_count=menu.submenus_count,
        dishes_count=menu.dishes_count,
    )


def submenuDC_to_pydantic_submenu_out(
    submenu: SubmenuDC, without_count: bool = False
) -> SubmenuOut | SubmenuOutWithoutCount:
    if without_count:
        return SubmenuOutWithoutCount(
            id=str(submenu.id),
            menu_id=submenu.menu_id,
            title=submenu.title,
            description=submenu.description,
        )
    return SubmenuOut(
        id=str(submenu.id),
        menu_id=submenu.menu_id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=submenu.dishes_count,
    )


def dishDC_to_pydantic_dish_out(dish: DishDC) -> DishOut:
    return DishOut(
        id=str(dish.id),
        menu_id=dish.menu_id,
        submenu_id=dish.menu_id,
        title=dish.title,
        description=dish.description,
        price=str(round(dish.price, 2)),
    )
