from crud.pydantic_models import (
    DishOut,
    MenuOut,
    MenuOutWithoutCount,
    SubmenuOut,
    SubmenuOutWithoutCount,
)
from dataclass import DishDC, MenuDC, SubmenuDC


def menuDC_to_pydantic_menu_out(
    menu: MenuDC
) -> MenuOut:
    return MenuOut(
        id=str(menu.id),
        title=menu.title,
        description=menu.description,
        submenus_count=menu.submenus_count,  # type: ignore
        dishes_count=menu.dishes_count,  # type: ignore
    )


def menuDC_to_pydantic_menu_out_no_count(
    menu: MenuDC
) -> MenuOutWithoutCount:
    return MenuOutWithoutCount(
        id=str(menu.id), title=menu.title, description=menu.description
    )


def submenuDC_to_pydantic_submenu_out(
    submenu: SubmenuDC
) -> SubmenuOut:
    return SubmenuOut(
        id=str(submenu.id),
        menu_id=submenu.menu_id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=submenu.dishes_count,  # type: ignore
    )


def submenuDC_to_pydantic_submenu_out_no_count(
    submenu: SubmenuDC
) -> SubmenuOutWithoutCount:
    return SubmenuOutWithoutCount(
        id=str(submenu.id),
        menu_id=submenu.menu_id,
        title=submenu.title,
        description=submenu.description,
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
