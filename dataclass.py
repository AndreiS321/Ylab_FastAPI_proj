from dataclasses import dataclass


@dataclass
class MenuDC:
    id: int
    title: str
    description: str
    submenus_count: int | None = None
    dishes_count: int | None = None


@dataclass
class SubmenuDC:
    id: int
    menu_id: int
    title: str
    description: str
    dishes_count: int | None = None


@dataclass
class DishDC:
    id: int
    menu_id: int
    submenu_id: int
    title: str
    description: str
    price: float
