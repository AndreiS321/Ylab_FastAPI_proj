from sqlalchemy import Float, ForeignKey, String, Text, distinct, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from crud.pydantic_models import DishOut, MenuOut, SubmenuOut
from sqlalchemy_base import db


class Menu(db):
    __tablename__ = 'menu'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    submenus: Mapped[list['Submenu']] = relationship(
        back_populates='menu', cascade='all, delete-orphan'
    )
    dishes: Mapped[list['Dish']] = relationship(
        back_populates='menu', cascade='all, delete-orphan'
    )

    async def to_pydantic_model(self, session: AsyncSession) -> MenuOut:
        smtm = (
            select(func.count(distinct(Submenu.id)), func.count(Dish.id))
            .select_from(Menu)
            .join(Submenu, Submenu.menu_id == Menu.id)
            .join(Dish, Dish.menu_id == Menu.id, isouter=True)
            .where(Menu.id == self.id)
        )
        count = (await session.execute(smtm)).one()
        menu_res = MenuOut(
            id=str(self.id),
            title=self.title,
            description=self.description,
            submenus_count=count[0],
            dishes_count=count[1],
        )
        return menu_res

    def __repr__(self) -> str:
        return f'Меню {self.title}'


class Submenu(db):
    __tablename__ = 'submenu'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    menu_id: Mapped[int] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'))
    menu: Mapped['Menu'] = relationship(back_populates='submenus')

    dishes: Mapped[list['Dish']] = relationship(
        back_populates='submenu', cascade='all, delete-orphan'
    )

    async def to_pydantic_model(self, session: AsyncSession) -> SubmenuOut:
        smtm = (
            select(func.count(Dish.id))
            .select_from(Submenu)
            .join(Dish, Dish.submenu_id == Submenu.id)
            .where(Submenu.id == self.id)
        )
        count = (await session.execute(smtm)).one()

        submenu_res = SubmenuOut(
            id=str(self.id),
            menu_id=self.menu_id,
            title=self.title,
            description=self.description,
            dishes_count=count[0],
        )
        return submenu_res

    def __repr__(self) -> str:
        return f'Подменю {self.title}'


class Dish(db):
    __tablename__ = 'dish'

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[float] = mapped_column(Float())

    menu_id: Mapped[int] = mapped_column(ForeignKey('menu.id', ondelete='CASCADE'))
    menu: Mapped['Menu'] = relationship(back_populates='dishes')

    submenu_id: Mapped[int] = mapped_column(
        ForeignKey('submenu.id', ondelete='CASCADE')
    )
    submenu: Mapped['Submenu'] = relationship(back_populates='dishes')

    async def to_pydantic_model(self, session: AsyncSession) -> DishOut:
        dish_res = DishOut(
            id=str(self.id),
            menu_id=self.menu_id,
            submenu_id=self.submenu_id,
            title=self.title,
            description=self.description,
            price=str(round(self.price, 2)),
        )
        return dish_res

    def __repr__(self) -> str:
        return f'Блюдо {self.title}'
