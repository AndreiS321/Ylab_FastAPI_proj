from fastapi import APIRouter, HTTPException

from crud.pydantic_models import MenuIn, MenuOutWithoutCount, MenuOut
from crud.utils import menuDC_to_pydantic_menu_out
from crud_db.menu import get_menu_db_list, get_menu_db, create_menu_db, patch_menu_db, delete_menu_db

router = APIRouter(prefix="/api/v1/menus",
                   tags=["menus"],
                   )


@router.get("/")
async def get_menu_list():
    return [menuDC_to_pydantic_menu_out(menu) for menu in await get_menu_db_list()]


@router.get("/{menu_id}")
async def get_menu(menu_id: int):
    res = await get_menu_db(menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return menuDC_to_pydantic_menu_out(res)


@router.post("/", status_code=201)
async def add_menu(menu: MenuIn) -> MenuOutWithoutCount:
    res = await create_menu_db(title=menu.title,
                               description=menu.description)
    return menuDC_to_pydantic_menu_out(res, without_count=True)


@router.patch("/{menu_id}")
async def patch_menu(menu_id: int, menu: MenuIn) -> MenuOut:
    res = await patch_menu_db(menu_id=menu_id,
                              title=menu.title,
                              description=menu.description)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return menuDC_to_pydantic_menu_out(res)


@router.delete("/{menu_id}")
async def delete_menu(menu_id: int) -> MenuOut:
    res = await delete_menu_db(menu_id=menu_id)
    if not res:
        raise HTTPException(status_code=404, detail="menu not found")
    return menuDC_to_pydantic_menu_out(res)
