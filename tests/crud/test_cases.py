import pytest
from sqlalchemy import select

from models import Menu, Submenu, Dish
from . import test_menu, test_submenu, test_dish
from ..test_objects import menu1, submenu1, dish1, dish2

pytestmark = pytest.mark.anyio


async def test_count(client, session):
    # Создание меню
    await test_menu.test_create(client, menu=menu1)
    created_menu = await session.scalar(select(Menu).where(Menu.title == menu1["title"]))

    # Создание подменю
    await test_submenu.test_create(client, session, submenu=submenu1, menu_id=created_menu.id)
    created_submenu = await session.scalar(select(Submenu).where(Submenu.title == submenu1["title"]))
    created_menu_dc = await Menu.menu_to_dc(created_menu, session)
    assert created_menu_dc.submenus_count == 1

    # Создание блюда 1
    await test_dish.test_create(client, session, dish=dish1,
                                menu_id=created_menu.id, submenu_id=created_submenu.id)
    created_dish1 = await session.scalar(select(Dish).where(Dish.title == dish1["title"]))
    created_menu_dc = await Menu.menu_to_dc(created_menu, session)
    assert created_menu_dc.submenus_count == 1
    assert created_menu_dc.dishes_count == 1

    # Создание блюда 2
    await test_dish.test_create(client, session, dish=dish2,
                                menu_id=created_menu.id, submenu_id=created_submenu.id)
    created_dish2 = await session.scalar(select(Dish).where(Dish.title == dish2["title"]))

    # Просмотр определённого меню
    await test_menu.test_get_menu(client, session, menu_id=created_menu.id)
    created_menu_dc = await Menu.menu_to_dc(created_menu, session)
    assert created_menu_dc.submenus_count == 1
    assert created_menu_dc.dishes_count == 2

    # Просмотр определённого подменю
    await test_submenu.test_get_submenu(client, session, menu_id=created_menu.id,
                                        submenu_id=created_submenu.id)
    created_submenu_dc = await Submenu.submenu_to_dc(created_submenu, session)
    assert created_submenu_dc.dishes_count == 2

    # Удаление подменю
    await test_submenu.test_delete(client, session,
                                   menu_id=created_menu.id, submenu_id=created_submenu.id)
    created_menu_dc = await Menu.menu_to_dc(created_menu, session)
    assert created_menu_dc.submenus_count == 0
    assert created_menu_dc.dishes_count == 0

    # Просмотр списка подменю
    await test_submenu.test_get_list(client, session, menu_id=created_menu.id)
    submenus = (await session.scalars(select(Submenu).where(Submenu.menu_id == created_menu.id))).all()
    assert submenus == []

    # Просмотр списка блюд
    await test_dish.test_get_list(client, session, menu_id=created_menu.id, submenu_id=created_submenu.id)
    dishes = (await session.scalars(select(Dish).where(Dish.menu_id == created_menu.id))).all()
    assert dishes == []

    # Просмотр определённого меню
    await test_menu.test_get_menu(client, session, menu_id=created_menu.id)
    created_menu_dc = await Menu.menu_to_dc(created_menu, session)
    assert created_menu_dc.submenus_count == 0
    assert created_menu_dc.dishes_count == 0

    # Удаление меню
    await test_menu.test_delete(client, session, menu_id=created_menu.id)
    created_menu = await session.scalar(select(Menu).where(Menu.id == created_menu_dc.id))
    assert created_menu is None

    # Просмотр списка меню
    await test_menu.test_get_list(client)
    menus = (await session.scalars(select(Menu))).all()
    assert menus == []
