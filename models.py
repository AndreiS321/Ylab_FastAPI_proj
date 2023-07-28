from typing import List

from sqlalchemy import String, Text, ForeignKey, Float, select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship

from dataclass import MenuDC, SubmenuDC, DishDC
from sqlalchemy_base import db


class Menu(db):
    __tablename__ = "menu"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    submenus: Mapped[List["Submenu"]] = relationship(
        back_populates="menu", cascade="all, delete-orphan"
    )
    dishes: Mapped[List["Dish"]] = relationship(
        back_populates="menu", cascade="all, delete-orphan"
    )

    @staticmethod
    async def menu_to_dc(menu: "Menu", session: AsyncSession) -> MenuDC:
        smtm = select(func.count(distinct(Submenu.id)), func.count(Dish.id)) \
            .select_from(Menu) \
            .join(Submenu, Submenu.menu_id == Menu.id) \
            .join(Dish, Dish.menu_id == Menu.id, isouter=True) \
            .where(Menu.id == menu.id)
        count = (await session.execute(smtm)).one_or_none()
        menu_res = MenuDC(id=menu.id,
                          title=menu.title,
                          description=menu.description,
                          submenus_count=count[0],
                          dishes_count=count[1])
        return menu_res


def __repr__(self) -> str:
    return f"Меню {self.title}"


class Submenu(db):
    __tablename__ = "submenu"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())

    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))
    menu: Mapped["Menu"] = relationship(back_populates="submenus")

    dishes: Mapped[List["Dish"]] = relationship(
        back_populates="submenu", cascade="all, delete-orphan"
    )

    @staticmethod
    async def submenu_to_dc(submenu: "Submenu", session: AsyncSession) -> SubmenuDC:
        smtm = select(func.count(Dish.id)) \
            .select_from(Submenu) \
            .join(Dish, Dish.submenu_id == Submenu.id) \
            .where(Submenu.id == submenu.id)
        count = (await session.execute(smtm)).one_or_none()

        submenu_res = SubmenuDC(id=submenu.id,
                                menu_id=submenu.menu_id,
                                title=submenu.title,
                                description=submenu.description,
                                dishes_count=count[0])
        return submenu_res

    def __repr__(self) -> str:
        return f"Подменю {self.title}"


class Dish(db):
    __tablename__ = "dish"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text())
    price: Mapped[float] = mapped_column(Float())

    menu_id: Mapped[int] = mapped_column(ForeignKey("menu.id", ondelete="CASCADE"))
    menu: Mapped["Menu"] = relationship(back_populates="dishes")

    submenu_id: Mapped[int] = mapped_column(ForeignKey("submenu.id", ondelete="CASCADE"))
    submenu: Mapped["Submenu"] = relationship(back_populates="dishes")

    @staticmethod
    async def dish_to_dc(dish: "Dish", session: AsyncSession) -> DishDC:
        dish_res = DishDC(id=dish.id,
                          menu_id=dish.menu_id,
                          submenu_id=dish.submenu_id,
                          title=dish.title,
                          description=dish.description,
                          price=dish.price)
        return dish_res

    def __repr__(self) -> str:
        return f"Блюдо {self.title}"
