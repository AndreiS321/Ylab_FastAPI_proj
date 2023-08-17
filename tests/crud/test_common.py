import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.crud.utils import create_dish, create_menu, create_submenu
from tests.test_objects import dish1, menu1, submenu1

base_url = '/api/v1/'
pytestmark = pytest.mark.anyio


async def test_get_objects_list_empty(client: AsyncClient):
    resp = await client.get(base_url, follow_redirects=True)
    assert resp.status_code == 200
    assert resp.json() == []


async def test_get_objects_list(client: AsyncClient, session: AsyncSession):
    menu = await create_menu(menu1, session, with_count=False, convert_types=False)
    menu_id = int(menu.id)
    submenu = await create_submenu(
        submenu1, menu_id, session, with_count=False, convert_types=False
    )
    submenu_id = int(submenu.id)
    dish = await create_dish(dish1, menu_id, submenu_id, session, convert_types=False)
    resp = await client.get(base_url, follow_redirects=True)
    assert resp.status_code == 200
    assert resp.json() == [
        {
            'menu': menu.as_dict,
            'submenus': [{'submenu': submenu.as_dict, 'dishes': [dish.as_dict]}],
        }
    ]
