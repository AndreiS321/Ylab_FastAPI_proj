from fastapi import APIRouter

router_menus = APIRouter(
    prefix='/api/v1/menus',
    tags=['menus'],
)

router_submenus = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus',
    tags=['submenus'],
)

router_dishes = APIRouter(
    prefix='/api/v1/menus/{menu_id}/submenus/{submenu_id}/dishes',
    tags=['dishes'],
)

router_common = APIRouter(prefix='/api/v1', tags=['common'])
