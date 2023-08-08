from crud.pydantic_models import DishOut, MenuOut, SubmenuOut
from dataclass import DishDC, MenuDC, SubmenuDC


def menuDC_to_pydantic_menu_out(menu: MenuDC | dict) -> MenuOut:
    menu = menu if isinstance(menu, MenuDC) else MenuDC.dict_to_dc(menu)
    return MenuOut(
        id=str(menu.id),
        title=menu.title,
        description=menu.description,
        submenus_count=menu.submenus_count,
        dishes_count=menu.dishes_count,
    )


def submenuDC_to_pydantic_submenu_out(submenu: SubmenuDC | dict) -> SubmenuOut:
    submenu = (
        submenu if isinstance(submenu, SubmenuDC) else SubmenuDC.dict_to_dc(submenu)
    )
    return SubmenuOut(
        id=str(submenu.id),
        menu_id=submenu.menu_id,
        title=submenu.title,
        description=submenu.description,
        dishes_count=submenu.dishes_count,
    )


def dishDC_to_pydantic_dish_out(dish: DishDC | dict) -> DishOut:
    dish = dish if isinstance(dish, DishDC) else DishDC.dict_to_dc(dish)
    return DishOut(
        id=str(dish.id),
        menu_id=dish.menu_id,
        submenu_id=dish.menu_id,
        title=dish.title,
        description=dish.description,
        price=str(round(dish.price, 2)),
    )
