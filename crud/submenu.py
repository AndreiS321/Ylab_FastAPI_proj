from fastapi import APIRouter, HTTPException

from crud.pydantic_models import SubmenuIn, SubmenuOutWithoutCount, SubmenuOut
from crud.utils import submenuDC_to_pydantic_submenu_out
from crud_db.submenu import create_submenu_db, get_submenu_db_list, get_submenu_db, patch_submenu_db, delete_submenu_db

router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus",
                   tags=["submenus"],
                   )


@router.get("/")
async def get_submenu_list(menu_id: int):
    return [submenuDC_to_pydantic_submenu_out(submenu) for submenu in await get_submenu_db_list(menu_id=menu_id)]


@router.get("/{submenu_id}")
async def get_submenu(menu_id: int, submenu_id: int):
    res = await get_submenu_db(submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenuDC_to_pydantic_submenu_out(res)


@router.post("/", status_code=201)
async def add_submenu(menu_id: int, submenu: SubmenuIn) -> SubmenuOutWithoutCount:
    res = await create_submenu_db(menu_id=menu_id,
                                  title=submenu.title,
                                  description=submenu.description)
    return submenuDC_to_pydantic_submenu_out(res, without_count=True)


@router.patch("/{submenu_id}")
async def patch_submenu(menu_id: int, submenu_id: int, submenu: SubmenuIn) -> SubmenuOut:
    res = await patch_submenu_db(submenu_id=submenu_id,
                                 title=submenu.title,
                                 description=submenu.description)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenuDC_to_pydantic_submenu_out(res)


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int) -> SubmenuOut:
    res = await delete_submenu_db(submenu_id=submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenuDC_to_pydantic_submenu_out(res)
