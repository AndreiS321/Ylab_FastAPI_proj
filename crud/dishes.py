from typing import List

from fastapi import HTTPException, Depends

from crud.pydantic_models import DishOut, DishIn
from crud.utils import dishDC_to_pydantic_dish_out
from crud_db.dishes import DishesAccessor
from .routers import router_dishes as router


@router.get("/")
async def get_dish_list(
    submenu_id: int, accessor: DishesAccessor = Depends(DishesAccessor)
) -> List[DishOut]:
    return [
        dishDC_to_pydantic_dish_out(dish)
        for dish in await accessor.get_list(submenu_id=submenu_id)
    ]


@router.get("/{dish_id}")
async def get_dish(
    dish_id: int, accessor: DishesAccessor = Depends(DishesAccessor)
) -> DishOut:
    res = await accessor.get(id=dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return dishDC_to_pydantic_dish_out(res)


@router.post("/", status_code=201)
async def add_dish(
    menu_id: int,
    submenu_id: int,
    dish: DishIn,
    accessor: DishesAccessor = Depends(DishesAccessor),
) -> DishOut:
    res = await accessor.create(
        menu_id=menu_id,
        submenu_id=submenu_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )
    return dishDC_to_pydantic_dish_out(res)


@router.patch("/{dish_id}")
async def patch_dish(
    dish_id: int, dish: DishIn, accessor: DishesAccessor = Depends(DishesAccessor)
) -> DishOut:
    res = await accessor.patch(
        dish_id=dish_id,
        title=dish.title,
        description=dish.description,
        price=dish.price,
    )
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return dishDC_to_pydantic_dish_out(res)


@router.delete("/{dish_id}")
async def delete_dish(
    dish_id: int, accessor: DishesAccessor = Depends(DishesAccessor)
) -> DishOut:
    res = await accessor.delete(dish_id=dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return dishDC_to_pydantic_dish_out(res)
