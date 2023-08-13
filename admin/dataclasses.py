from pydantic import BaseModel


class ExcelDish(BaseModel):
    id: int | None = None
    title: str
    description: str
    price: float

    @property
    def as_dict(self):
        return self.model_dump(mode="python")


class ExcelSubmenu(BaseModel):
    id: int | None = None
    title: str
    description: str
    dishes: list[ExcelDish]

    @property
    def as_dict(self):
        return self.model_dump(mode="python")


class ExcelMenu(BaseModel):
    id: int | None = None
    title: str
    description: str
    submenus: list[ExcelSubmenu]

    @property
    def as_dict(self):
        return self.model_dump(mode="python")
