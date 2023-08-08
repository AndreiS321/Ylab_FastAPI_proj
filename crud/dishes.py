from fastapi import Depends, HTTPException

from crud.pydantic_models import DishIn, DishOut
from crud.utils import dishDC_to_pydantic_dish_out
from crud_db.dishes import DishesAccessor

from .routers import router_dishes as router


@router.get('/')
async def get_dish_list(
    menu_id: int, submenu_id: int, accessor: DishesAccessor = Depends(DishesAccessor)
) -> list[DishOut]:
    return [
        dishDC_to_pydantic_dish_out(dish)
        for dish in await accessor.get_list(
            menu_id=menu_id,
            submenu_id=submenu_id,
        )
    ]


@router.get('/{dish_id}')
async def get_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    accessor: DishesAccessor = Depends(DishesAccessor),
) -> DishOut:
    res = await accessor.get(menu_id=menu_id, submenu_id=submenu_id, dish_id=dish_id)
    if not res:
        raise HTTPException(status_code=404, detail='dish not found')
    return dishDC_to_pydantic_dish_out(res)


@router.post('/', status_code=201)
async def add_dish(
    menu_id: int,
    submenu_id: int,
    dish: DishIn,
    accessor: DishesAccessor = Depends(DishesAccessor),
) -> DishOut:
    res = await accessor.create(
        dish.title,
        dish.description,
        dish.price,
        menu_id=menu_id,
        submenu_id=submenu_id,
    )
    return dishDC_to_pydantic_dish_out(res)


@router.patch('/{dish_id}')
async def patch_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    dish: DishIn,
    accessor: DishesAccessor = Depends(DishesAccessor),
) -> DishOut:
    res = await accessor.patch(
        dish.title,
        dish.description,
        dish.price,
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
    if not res:
        raise HTTPException(status_code=404, detail='dish not found')
    return dishDC_to_pydantic_dish_out(res)


@router.delete('/{dish_id}')
async def delete_dish(
    menu_id: int,
    submenu_id: int,
    dish_id: int,
    accessor: DishesAccessor = Depends(DishesAccessor),
) -> DishOut:
    res = await accessor.delete(
        menu_id=menu_id,
        submenu_id=submenu_id,
        dish_id=dish_id,
    )
    if not res:
        raise HTTPException(status_code=404, detail='dish not found')
    return dishDC_to_pydantic_dish_out(res)
