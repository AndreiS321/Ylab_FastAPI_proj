from fastapi import BackgroundTasks, Depends, HTTPException

from crud.pydantic_models import MenuIn, MenuOut
from crud.routers import router_menus as router
from crud_db.menu import MenusAccessor


@router.get('/')
async def get_menu_list(
    accessor: MenusAccessor = Depends(MenusAccessor),
) -> list[MenuOut]:
    return await accessor.get_list()


@router.get('/{menu_id}')
async def get_menu(
    menu_id: int, accessor: MenusAccessor = Depends(MenusAccessor)
) -> MenuOut:
    res = await accessor.get(menu_id=menu_id)
    if not res:
        raise HTTPException(status_code=404, detail='menu not found')
    return res


@router.post('/', status_code=201)
async def add_menu(
    menu: MenuIn,
    background_tasks: BackgroundTasks,
    accessor: MenusAccessor = Depends(MenusAccessor),
) -> MenuOut:
    res = await accessor.create(
        menu.title, menu.description, background_tasks=background_tasks
    )
    return res


@router.patch('/{menu_id}')
async def patch_menu(
    menu_id: int,
    menu: MenuIn,
    background_tasks: BackgroundTasks,
    accessor: MenusAccessor = Depends(MenusAccessor),
) -> MenuOut:
    res = await accessor.patch(
        menu.title, menu.description, menu_id=menu_id, background_tasks=background_tasks
    )
    if not res:
        raise HTTPException(status_code=404, detail='menu not found')
    return res


@router.delete('/{menu_id}')
async def delete_menu(
    menu_id: int,
    background_tasks: BackgroundTasks,
    accessor: MenusAccessor = Depends(MenusAccessor),
) -> MenuOut:
    res = await accessor.delete(menu_id=menu_id, background_tasks=background_tasks)
    if not res:
        raise HTTPException(status_code=404, detail='menu not found')
    return res
