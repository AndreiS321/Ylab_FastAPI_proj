from typing import List

from fastapi import APIRouter, HTTPException

from crud.pydantic_models import DishOut, DishIn
from crud_db.dishes import get_dish_db_list, get_dish_db, create_dish_db, patch_dish_db, delete_dish_db

router = APIRouter(prefix="/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes",
                   tags=["dishes"],
                   )


@router.get("/")
async def get_dish_list(menu_id: int, submenu_id: int) -> List[DishOut]:
    return [DishOut(id=dish.id,
                    menu_id=dish.menu_id,
                    submenu_id=dish.submenu_id,
                    title=dish.title,
                    description=dish.description,
                    price=dish.price,
                    ) for dish in await get_dish_db_list(submenu_id=submenu_id)]


@router.get("/{dish_id}")
async def get_dish(menu_id: int, submenu_id: int, dish_id: int) -> DishOut:
    res = await get_dish_db(dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return DishOut(id=res.id,
                   menu_id=res.menu_id,
                   submenu_id=res.menu_id,
                   title=res.title,
                   description=res.description,
                   price=res.price,
                   )


@router.post("/", status_code=201)
async def add_dish(menu_id: int, submenu_id: int, dish: DishIn) -> DishOut:
    res = await create_dish_db(menu_id=menu_id,
                               submenu_id=submenu_id,
                               title=dish.title,
                               description=dish.description,
                               price=dish.price,
                               )
    return DishOut(id=res.id,
                   menu_id=res.menu_id,
                   submenu_id=res.menu_id,
                   title=res.title,
                   description=res.description,
                   price=res.price,
                   )


@router.patch("/{dish_id}")
async def patch_dish(menu_id: int, submenu_id: int, dish_id: int, dish: DishIn) -> DishOut:
    res = await patch_dish_db(dish_id=dish_id,
                              title=dish.title,
                              description=dish.description,
                              price=dish.price,
                              )
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return DishOut(id=res.id,
                   menu_id=res.menu_id,
                   submenu_id=res.menu_id,
                   title=res.title,
                   description=res.description,
                   price=res.price,
                   )


@router.delete("/{dish_id}")
async def delete_dish(menu_id: int, submenu_id: int, dish_id: int) -> DishOut:
    res = await delete_dish_db(dish_id=dish_id)
    if not res:
        raise HTTPException(status_code=404, detail="dish not found")
    return DishOut(id=res.id,
                   menu_id=res.menu_id,
                   submenu_id=res.menu_id,
                   title=res.title,
                   description=res.description,
                   price=res.price,
                   )
