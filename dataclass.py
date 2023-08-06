from dataclasses import asdict, dataclass
from json import dumps


@dataclass
class MenuDC:
    id: int
    title: str
    description: str
    submenus_count: int
    dishes_count: int

    @staticmethod
    def dict_to_dc(dct: dict) -> 'MenuDC':
        return MenuDC(**dct)

    @property
    def as_json(self):
        return dumps(asdict(self))

    @property
    def as_dict(self):
        return asdict(self)


@dataclass
class SubmenuDC:
    id: int
    menu_id: int
    title: str
    description: str
    dishes_count: int

    @staticmethod
    def dict_to_dc(dct: dict) -> 'SubmenuDC':
        return SubmenuDC(**dct)

    @property
    def as_json(self):
        return dumps(asdict(self))

    @property
    def as_dict(self):
        return asdict(self)


@dataclass
class DishDC:
    id: int
    menu_id: int
    submenu_id: int
    title: str
    description: str
    price: float

    @staticmethod
    def dict_to_dc(dct: dict) -> 'DishDC':
        return DishDC(**dct)

    @property
    def as_json(self):
        return dumps(asdict(self))

    @property
    def as_dict(self):
        return asdict(self)
