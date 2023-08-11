from json import dumps, loads

from app import app
from crud.pydantic_models import DishOut, MenuOut, MenuOutList, SubmenuOut


async def delete_related_cache_menu(obj: MenuOut):
    # Удаление кэша списка меню
    await app.redis.delete(MenuOut.__name__)

    # Удаление кэша меню
    name = get_cache_name(MenuOut.__name__, menu_id=obj.id)
    await app.redis.delete(name)

    # Удаление списка подменю и подменю, которые были в меню
    async for key in app.redis.scan_iter(f'{SubmenuOut.__name__}menu_id{obj.id}*'):
        await app.redis.delete(key)

    # Удаление списка блюд и блюд, которые были в меню
    async for key in app.redis.scan_iter(f'{DishOut.__name__}menu_id{obj.id}*'):
        await app.redis.delete(key)


async def delete_related_cache_submenu(obj: SubmenuOut):
    # Удаление кэша списка меню
    await app.redis.delete(MenuOut.__name__)

    # Удаление кэша меню
    name = get_cache_name(MenuOut.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша списка подменю
    name = get_cache_name(SubmenuOut.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша подменю
    name = get_cache_name(SubmenuOut.__name__, menu_id=obj.menu_id, submenu_id=obj.id)
    await app.redis.delete(name)

    # Удаление списка блюд и блюд, которые были в меню
    async for key in app.redis.scan_iter(
        f'{DishOut.__name__}menu_id{obj.menu_id}submenu_id{obj.id}*'
    ):
        await app.redis.delete(key)


async def delete_related_cache_dish(obj: DishOut):
    # Удаление кэша списка меню
    await app.redis.delete(MenuOut.__name__)

    # Удаление кэша меню
    name = get_cache_name(MenuOut.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша списка подменю
    name = get_cache_name(SubmenuOut.__name__, menu_id=obj.menu_id)
    await app.redis.delete(name)

    # Удаление кэша подменю
    name = get_cache_name(
        SubmenuOut.__name__, menu_id=obj.menu_id, submenu_id=obj.submenu_id
    )
    await app.redis.delete(name)

    # Удаление кэша списка блюд
    name = get_cache_name(
        DishOut.__name__, menu_id=obj.menu_id, submenu_id=obj.submenu_id
    )
    await app.redis.delete(name)

    # Удаление кэша блюда
    name = get_cache_name(
        DishOut.__name__, menu_id=obj.menu_id, submenu_id=obj.submenu_id, dish_id=obj.id
    )
    await app.redis.delete(name)


async def delete_related_cache_common(obj):
    # Удаление кэша списка всех объектов
    await app.redis.delete(MenuOutList.__name__)


async def delete_related_cache(obj: MenuOut | SubmenuOut | DishOut):
    if isinstance(obj, MenuOut):
        await delete_related_cache_menu(obj)
    elif isinstance(obj, SubmenuOut):
        await delete_related_cache_submenu(obj)
    elif isinstance(obj, DishOut):
        await delete_related_cache_dish(obj)
    await delete_related_cache_common(obj)


def get_model_cache_name(obj: MenuOut | SubmenuOut | DishOut):
    class_name = obj.__class__.__name__
    if isinstance(obj, MenuOut):
        return f'{class_name}menu_id{obj.id}'
    elif isinstance(obj, SubmenuOut):
        return f'{class_name}menu_id{obj.menu_id}submenu_id{obj.id}'
    elif isinstance(obj, DishOut):
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
            name = get_cache_name(self.pydantic_model.__name__, **kwargs)
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
            name = get_cache_name(self.pydantic_model.__name__, **kwargs)
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
            name = get_model_cache_name(result)
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
