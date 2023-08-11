from string import Template

import pytest
from sqlalchemy import select

from models import Menu
from tests.crud.utils import create_menu
from tests.test_objects import menu1, menu1_updated

base_url = '/api/v1/menus'
url_template = Template(f'{base_url}/$menu_id')
pytestmark = pytest.mark.anyio


async def test_get_list(client):
    resp = await client.get(base_url, follow_redirects=True)

    assert resp.status_code == 200


async def test_get_menu(client, session, menu_id: int | None = None):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    resp = await client.get(
        url_template.substitute(menu_id=menu_id), follow_redirects=True
    )
    assert resp.status_code == 200
    json_resp = resp.json()
    assert json_resp['id'] == str(menu_id)


async def test_create(client, menu: dict | None = None):
    menu = menu if menu else menu1
    resp = await client.post('/api/v1/menus', json=menu1, follow_redirects=True)

    assert resp.status_code == 201
    json_resp = resp.json()
    assert (
        json_resp['title'] == menu1['title']
        and json_resp['description'] == menu1['description']
    )


async def test_patch(
    client, session, menu_id: int | None = None, menu_updated: dict | None = None
):
    menu_updated = menu_updated if menu_updated else menu1
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    resp = await client.patch(
        url_template.substitute(menu_id=menu_id),
        json=menu1_updated,
        follow_redirects=True,
    )

    assert resp.status_code == 200
    json_resp = resp.json()
    assert (
        json_resp['title'] == menu1_updated['title']
        and json_resp['description'] == menu1_updated['description']
    )


async def test_delete(client, session, menu_id: int | None = None):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    resp = await client.delete(
        url_template.substitute(menu_id=menu_id), follow_redirects=True
    )

    assert resp.status_code == 200
    menu = await session.scalar(select(Menu).where(Menu.id == menu_id))
    assert menu is None
