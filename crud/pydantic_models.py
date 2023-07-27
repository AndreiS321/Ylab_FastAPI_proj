from pydantic import BaseModel


class MenuIn(BaseModel):
    title: str
    description: str


class MenuOut(BaseModel):
    id: str
    title: str
    description: str
    submenus_count: int
    dishes_count: int


class MenuOutWithoutCount(BaseModel):
    id: str
    title: str
    description: str


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuOut(BaseModel):
    id: str
    menu_id: int
    title: str
    description: str
    dishes_count: int


class SubmenuOutWithoutCount(BaseModel):
    id: str
    menu_id: int
    title: str
    description: str


class DishIn(BaseModel):
    title: str
    description: str
    price: float


class DishOut(BaseModel):
    id: str
    menu_id: int
    submenu_id: int
    title: str
    description: str
    price: str
