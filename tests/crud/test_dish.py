from string import Template

import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Dish
from tests.crud.utils import create_dish, create_menu, create_submenu
from tests.test_objects import dish1, dish1_updated, menu1, submenu1

base_url = '/api/v1/menus'
url_template = Template(base_url + '/${menu_id}/submenus/${submenu_id}/dishes')
url_template_dish = Template(
    base_url + '/${menu_id}/submenus/${submenu_id}/dishes/${dish_id}'
)
pytestmark = pytest.mark.anyio


async def test_get_list(
    client: AsyncClient, session: AsyncSession, menu_id: int | None = None, submenu_id: int | None = None
):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    resp = await client.get(
        url_template.substitute(menu_id=menu_id, submenu_id=submenu_id),
        follow_redirects=True,
    )
    assert resp.status_code == 200


async def test_get_dish(
    client: AsyncClient,
    session: AsyncSession,
    menu_id: int | None = None,
    submenu_id: int | None = None,
    dish_id: int | None = None,
):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    if dish_id is None:
        dish = await create_dish(dish1, menu_id, submenu_id, session)
        dish_id = dish.id
    resp = await client.get(
        url_template_dish.substitute(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        ),
        follow_redirects=True,
    )

    assert resp.status_code == 200
    json_resp = resp.json()
    assert json_resp['id'] == str(dish_id) and json_resp['menu_id'] == menu_id


async def test_create(
    client: AsyncClient,
    session: AsyncSession,
    menu_id: int | None = None,
    submenu_id: int | None = None,
    dish: dict | None = None,
):
    dish = dish if dish else dish1
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    resp = await client.post(
        url_template.substitute(menu_id=menu_id, submenu_id=submenu_id),
        json=dish,
        follow_redirects=True,
    )

    assert resp.status_code == 201
    json_resp = resp.json()
    assert (
        json_resp['title'] == dish['title']
        and json_resp['menu_id'] == menu_id
        and json_resp['submenu_id'] == submenu_id
        and json_resp['price'] == dish['price']
        and json_resp['description'] == dish['description']
    )


async def test_patch(
    client: AsyncClient,
    session: AsyncSession,
    menu_id: int | None = None,
    submenu_id: int | None = None,
    dish_id: int | None = None,
    dish_updated: dict | None = None,
):
    dish_updated = dish_updated if dish_updated else dish1_updated
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    if dish_id is None:
        dish = await create_dish(dish1, menu_id, submenu_id, session)
        dish_id = dish.id
    resp = await client.patch(
        url_template_dish.substitute(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        ),
        json=dish_updated,
        follow_redirects=True,
    )

    assert resp.status_code == 200
    json_resp = resp.json()
    assert (
        json_resp['title'] == dish_updated['title']
        and json_resp['description'] == dish_updated['description']
        and json_resp['price'] == dish_updated['price']
    )


async def test_delete(
    client: AsyncClient,
    session: AsyncSession,
    menu_id: int | None = None,
    submenu_id: int | None = None,
    dish_id: int | None = None,
):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    if dish_id is None:
        dish = await create_dish(dish1, menu_id, submenu_id, session)
        dish_id = dish.id
    resp = await client.delete(
        url_template_dish.substitute(
            menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id
        ),
        follow_redirects=True,
    )

    assert resp.status_code == 200
    dish = await session.scalar(select(Dish).where(Dish.id == dish_id))
    assert dish is None
