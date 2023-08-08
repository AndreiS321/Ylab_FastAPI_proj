from json import dumps, loads

from fastapi import Depends

from app import app
from dataclass import DishDC, MenuDC, SubmenuDC
from db import get_session


async def delete_related_cache_menu(obj: MenuDC):
    # Удаление кэша списка меню
    await app.redis.delete(MenuDC.__name__)

    # Удаление кэша меню
    name = get_cache_name(MenuDC.__name__, menu_id=obj.id)
    await app.redis.delete(name)

    # Удаление списка подменю и подменю, которые были в меню
    async for key in app.redis.scan_iter(f'{SubmenuDC.__name__}menu_id{obj.id}*'):
        await app.redis.delete(key)

    # Удаление списка блюд и блюд, которые были в меню
    async for key in app.redis.scan_iter(f'{DishDC.__name__}menu_id{obj.id}*'):
        await app.redis.delete(key)


async def delete_related_cache_submenu(obj: SubmenuDC):
    # Удаление кэша списка меню
    await app.redis.delete(MenuDC.__name__)

    # Удаление кэша меню
    name = get_cache_name(MenuDC.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша списка подменю
    name = get_cache_name(SubmenuDC.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша подменю
    name = get_cache_name(SubmenuDC.__name__, menu_id=obj.menu_id, submenu_id=obj.id)
    await app.redis.delete(name)

    # Удаление списка блюд и блюд, которые были в меню
    async for key in app.redis.scan_iter(
        f'{DishDC.__name__}menu_id{obj.menu_id}submenu_id{obj.id}*'
    ):
        await app.redis.delete(key)


async def delete_related_cache_dish(obj: DishDC):
    # Удаление кэша списка меню
    await app.redis.delete(MenuDC.__name__)

    # Удаление кэша меню
    name = get_cache_name(MenuDC.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша списка подменю
    name = get_cache_name(SubmenuDC.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша подменю
    name = get_cache_name(
        SubmenuDC.__name__, menu_id=obj.menu_id, submenu_id=obj.submenu_id
    )
    await app.redis.delete(name)

    # Удаление кэша списка блюд
    name = get_cache_name(
        DishDC.__name__, menu_id=obj.menu_id, submenu_id=obj.submenu_id
    )
    await app.redis.delete(name)

    # Удаление кэша блюда
    name = get_cache_name(
        DishDC.__name__, menu_id=obj.menu_id, submenu_id=obj.submenu_id, dish_id=obj.id
    )
    await app.redis.delete(name)


async def delete_related_cache(obj: DishDC | SubmenuDC | MenuDC):
    if isinstance(obj, MenuDC):
        await delete_related_cache_menu(obj)
    elif isinstance(obj, SubmenuDC):
        await delete_related_cache_submenu(obj)
    elif isinstance(obj, DishDC):
        await delete_related_cache_dish(obj)


def get_dataclass_cache_name(obj: MenuDC | SubmenuDC | DishDC):
    class_name = obj.__class__.__name__
    if isinstance(obj, MenuDC):
        return f'{class_name}menu_id{obj.id}'
    elif isinstance(obj, SubmenuDC):
        return f'{class_name}menu_id{obj.menu_id}submenu_id{obj.id}'
    elif isinstance(obj, DishDC):
        return (
            f'{class_name}menu_id{obj.menu_id}submenu_id{obj.submenu_id}dish_id{obj.id}'
        )


def get_cache_name(class_name, *args, **kwargs):
    return (
        class_name
        + ''.join(str(i) for i in args)
        + ''.join(str(i) + str(j) for i, j in kwargs.items())
    )


def cache_get_all(seconds: int = 10):
    def wrapper1(func):
        async def wrapper2(self, *args, **kwargs):
            name = get_cache_name(self.dataclass.__name__, **kwargs)
            redis_value = await app.redis.get(name)
            if redis_value:
                redis_value = loads(redis_value)
                return redis_value or []

            result = await func(self, *args, **kwargs)
            if result is None:
                await app.redis.set(name, 'null', ex=seconds)
                return []
            await app.redis.set(
                name, dumps([res.as_dict for res in result]), ex=seconds
            )
            return result

        return wrapper2

    return wrapper1


def cache_get(seconds: int = 10):
    def wrapper1(func):
        async def wrapper2(self, *args, **kwargs):
            name = get_cache_name(self.dataclass.__name__, **kwargs)
            redis_value = await app.redis.get(name)
            if redis_value:
                redis_value = loads(redis_value)
                return redis_value
            result = await func(self, *args, **kwargs)
            if result is None:
                await app.redis.set(name, 'null', ex=seconds)
                return None
            await app.redis.set(name, result.as_json, ex=seconds)
            return result

        return wrapper2

    return wrapper1


def cache_post(seconds: int = 10):
    def wrapper1(func):
        async def wrapper2(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            if result is None:
                return None
            await delete_related_cache(result)
            name = get_cache_name(get_dataclass_cache_name(result))
            await app.redis.set(name, result.as_json, ex=seconds)
            return result

        return wrapper2

    return wrapper1


def cache_delete(func):
    async def wrapper2(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)
        if result is None:
            return None
        await delete_related_cache(result)
        return result

    return wrapper2


class BaseAccessor:
    def __init__(self, session=Depends(get_session)):
        self._session = session
