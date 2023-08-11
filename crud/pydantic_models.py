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

    @property
    def as_json(self):
        return self.model_dump_json()

    @property
    def as_dict(self):
        return self.model_dump(mode='python')


class SubmenuIn(BaseModel):
    title: str
    description: str


class SubmenuOut(BaseModel):
    id: str
    menu_id: int
    title: str
    description: str
    dishes_count: int

    @property
    def as_json(self):
        return self.model_dump_json()

    @property
    def as_dict(self):
        return self.model_dump(mode='python')


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

    @property
    def as_json(self):
        return self.model_dump_json()

    @property
    def as_dict(self):
        return self.model_dump(mode='python')


# class ObjectsList(BaseModel):
#     Men
