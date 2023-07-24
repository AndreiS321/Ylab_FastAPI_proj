from typing import List

from sqlalchemy import String, Text, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    def __repr__(self) -> str:
        return f"Блюдо {self.title}"
