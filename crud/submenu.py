from typing import List

from fastapi import HTTPException, Depends

from crud.pydantic_models import SubmenuIn, SubmenuOutWithoutCount, SubmenuOut
from crud.utils import submenuDC_to_pydantic_submenu_out
from crud_db.submenu import SubmenusAccessor
from .routers import router_submenus as router


@router.get("/")
async def get_submenu_list(
    menu_id: int, accessor: SubmenusAccessor = Depends(SubmenusAccessor)
) -> List[SubmenuOut]:
    return [
        submenuDC_to_pydantic_submenu_out(submenu)
        for submenu in await accessor.get_list(menu_id=menu_id)
    ]


@router.get("/{submenu_id}")
async def get_submenu(
    submenu_id: int, accessor: SubmenusAccessor = Depends(SubmenusAccessor)
) -> SubmenuOut:
    res = await accessor.get(id=submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenuDC_to_pydantic_submenu_out(res)


@router.post("/", status_code=201)
async def add_submenu(
    menu_id: int,
    submenu: SubmenuIn,
    accessor: SubmenusAccessor = Depends(SubmenusAccessor),
) -> SubmenuOutWithoutCount:
    res = await accessor.create(
        menu_id=menu_id, title=submenu.title, description=submenu.description
    )
    return submenuDC_to_pydantic_submenu_out(res, without_count=True)


@router.patch("/{submenu_id}")
async def patch_submenu(
    submenu_id: int,
    submenu: SubmenuIn,
    accessor: SubmenusAccessor = Depends(SubmenusAccessor),
) -> SubmenuOut:
    res = await accessor.patch(
        submenu_id=submenu_id, title=submenu.title, description=submenu.description
    )
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenuDC_to_pydantic_submenu_out(res)


@router.delete("/{submenu_id}")
async def delete_submenu(
    submenu_id: int, accessor: SubmenusAccessor = Depends(SubmenusAccessor)
) -> SubmenuOut:
    res = await accessor.delete(submenu_id=submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail="submenu not found")
    return submenuDC_to_pydantic_submenu_out(res)
