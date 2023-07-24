from fastapi import APIRouter, HTTPException

from crud.pydantic_models import SubmenuIn, SubmenuOutWithoutCount, SubmenuOut
from crud_db.submenu import create_submenu_db, get_submenu_db_list, get_submenu_db, patch_submenu_db, delete_submenu_db

router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus",
                   tags=["submenus"],
                   )


@router.get("/")
async def get_submenu_list(menu_id: int):
    return [SubmenuOut(id=submenu.id,
                       menu_id=submenu.menu_id,
                       title=submenu.title,
                       description=submenu.description,
                       dishes_count=submenu.dishes_count,
                       ) for submenu in await get_submenu_db_list(menu_id=menu_id)]


@router.get("/{submenu_id}")
async def get_submenu(menu_id: int, submenu_id: int):
    res = await get_submenu_db(submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return SubmenuOut(id=res.id,
                      menu_id=res.menu_id,
                      title=res.title,
                      description=res.description,
                      dishes_count=res.dishes_count,
                      )


@router.post("/", status_code=201)
async def add_submenu(menu_id: int, submenu: SubmenuIn) -> SubmenuOutWithoutCount:
    res = await create_submenu_db(menu_id=menu_id,
                                  title=submenu.title,
                                  description=submenu.description)
    return SubmenuOutWithoutCount(id=res.id,
                                  menu_id=res.menu_id,
                                  title=res.title,
                                  description=res.description)


@router.patch("/{submenu_id}")
async def patch_submenu(menu_id: int, submenu_id: int, submenu: SubmenuIn) -> SubmenuOut:
    res = await patch_submenu_db(submenu_id=submenu_id,
                                 title=submenu.title,
                                 description=submenu.description)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return SubmenuOut(id=res.id,
                      menu_id=res.menu_id,
                      title=res.title,
                      description=res.description,
                      dishes_count=res.dishes_count,
                      )


@router.delete("/{submenu_id}")
async def delete_submenu(menu_id: int, submenu_id: int) -> SubmenuOut:
    res = await delete_submenu_db(submenu_id=submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return SubmenuOut(id=res.id,
                      menu_id=res.menu_id,
                      title=res.title,
                      description=res.description,
                      dishes_count=res.dishes_count,
                      )
