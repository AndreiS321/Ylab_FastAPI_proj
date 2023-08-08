from fastapi import Depends, HTTPException

from crud.pydantic_models import SubmenuIn, SubmenuOut
from crud.utils import submenuDC_to_pydantic_submenu_out
from crud_db.submenu import SubmenusAccessor

from .routers import router_submenus as router


@router.get('/')
async def get_submenu_list(
    menu_id: int, accessor: SubmenusAccessor = Depends(SubmenusAccessor)
) -> list[SubmenuOut]:
    return [
        submenuDC_to_pydantic_submenu_out(submenu)
        for submenu in await accessor.get_list(menu_id=menu_id)
    ]


@router.get('/{submenu_id}')
async def get_submenu(
    menu_id: int,
    submenu_id: int,
    accessor: SubmenusAccessor = Depends(SubmenusAccessor),
) -> SubmenuOut:
    res = await accessor.get(menu_id=menu_id, submenu_id=submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenuDC_to_pydantic_submenu_out(res)


@router.post('/', status_code=201)
async def add_submenu(
    menu_id: int,
    submenu: SubmenuIn,
    accessor: SubmenusAccessor = Depends(SubmenusAccessor),
) -> SubmenuOut:
    res = await accessor.create(
        submenu.title,
        submenu.description,
        menu_id=menu_id,
    )
    return submenuDC_to_pydantic_submenu_out(res)


@router.patch('/{submenu_id}')
async def patch_submenu(
    menu_id: int,
    submenu_id: int,
    submenu: SubmenuIn,
    accessor: SubmenusAccessor = Depends(SubmenusAccessor),
) -> SubmenuOut:
    res = await accessor.patch(
        submenu.title,
        submenu.description,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    if not res:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenuDC_to_pydantic_submenu_out(res)


@router.delete('/{submenu_id}')
async def delete_submenu(
    menu_id: int,
    submenu_id: int,
    accessor: SubmenusAccessor = Depends(SubmenusAccessor),
) -> SubmenuOut:
    res = await accessor.delete(menu_id=menu_id, submenu_id=submenu_id)
    if not res:
        raise HTTPException(status_code=404, detail='submenu not found')
    return submenuDC_to_pydantic_submenu_out(res)
