from string import Template

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Submenu
from tests.crud.utils import create_submenu, create_menu
from tests.test_objects import menu1, submenu1, submenu1_updated

base_url = "/api/v1/menus"
url_template = Template(base_url + "/${menu_id}/submenus")
url_template_submenu = Template(base_url + "/${menu_id}/submenus/${submenu_id}")
pytestmark = pytest.mark.anyio


async def test_get_list(client, session, menu_id: int = None):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    resp = await client.get(url_template.substitute(menu_id=menu_id), follow_redirects=True)

    assert resp.status_code == 200


async def test_get_submenu(client, session, menu_id: int = None, submenu_id: int = None):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    resp = await client.get(url_template_submenu.substitute(menu_id=menu_id, submenu_id=submenu_id),
                            follow_redirects=True)

    assert resp.status_code == 200
    json_resp = resp.json()
    assert json_resp["id"] == str(submenu_id) and \
           json_resp["menu_id"] == menu_id


async def test_create(client, session, menu_id: int = None, submenu: dict = None):
    submenu = submenu if submenu else submenu1
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    resp = await client.post(url_template.substitute(menu_id=menu_id),
                             json=submenu,
                             follow_redirects=True)

    assert resp.status_code == 201
    json_resp = resp.json()
    assert json_resp["title"] == submenu["title"] and \
           json_resp["menu_id"] == menu_id and \
           json_resp["description"] == submenu["description"]


async def test_patch(client, session, menu_id: int = None, submenu_id: int = None,
                     submenu_updated: dict = None):
    submenu_updated = submenu_updated if submenu_updated else submenu1_updated
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    resp = await client.patch(url_template_submenu.substitute(menu_id=menu_id,
                                                              submenu_id=submenu_id),
                              json=submenu_updated,
                              follow_redirects=True)

    assert resp.status_code == 200
    json_resp = resp.json()
    assert json_resp["title"] == submenu_updated["title"] and \
           json_resp["description"] == submenu_updated["description"]


async def test_delete(client, session: AsyncSession, menu_id: int = None, submenu_id: int = None):
    if menu_id is None:
        menu = await create_menu(menu1, session)
        menu_id = menu.id
    if submenu_id is None:
        submenu = await create_submenu(submenu1, menu_id, session)
        submenu_id = submenu.id
    resp = await client.delete(url_template_submenu.substitute(menu_id=menu_id, submenu_id=submenu_id),
                               follow_redirects=True)

    assert resp.status_code == 200
    submenu = await session.scalar(select(Submenu).where(Submenu.id == submenu_id))
    assert submenu is None
