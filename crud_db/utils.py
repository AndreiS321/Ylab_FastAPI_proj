from json import dumps, loads

from fastapi import Depends

from app import app
from db import get_session


def get_cache_name(class_name, *args, **kwargs):
    return (
        class_name
        + ''.join(str(i) for i in args)
        + ''.join(str(i) + str(j) for i, j in kwargs.items())
    )

# Кэш запросов к спискам объектов
def cache_get_all(seconds: int = 10):
    def wrapper1(func):
        async def wrapper2(self, *args, **kwargs):
            name = get_cache_name(self.__class__.__name__, *args, **kwargs)
            redis_value = await app.redis.get(name)
            print(name, redis_value, end=' ')
            if redis_value:
                redis_value = loads(redis_value)
                return redis_value or []
            result = await func(self, *args, **kwargs)
            print(result)
            if result is None:
                await app.redis.set(name, 'null', ex=seconds)
                return []
            await app.redis.set(
                name, dumps([res.as_dict for res in result]), ex=seconds
            )
            return result

        return wrapper2

    return wrapper1

# Кэш запросов к определённому объекту
def cache_get(seconds: int = 10):
    def wrapper1(func):
        async def wrapper2(self, *args, **kwargs):
            name = get_cache_name(self.__class__.__name__, *args, **kwargs)
            redis_value = await app.redis.get(name)
            print(name, redis_value, end=' ')
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

# Обновление кэша при добавлении объекта
def cache_post(seconds: int = 10):
    def wrapper1(func):
        async def wrapper2(self, *args, **kwargs):
            result = await func(self, *args, **kwargs)
            if result is None:
                return None
            name = get_cache_name(self.__class__.__name__, id=result.id)
            print(name, result, end=' ')
            await app.redis.set(name, result.as_json, ex=seconds)
            return result

        return wrapper2

    return wrapper1

# Удаление кэша при добавлении объекта
def cache_delete(func):
    async def wrapper2(self, *args, **kwargs):
        result = await func(self, *args, **kwargs)
        if result is None:
            return None
        name = get_cache_name(self.__class__.__name__, id=result.id)
        redis_value = await app.redis.get(name)
        if redis_value:
            await app.redis.delete(name)
        return result

    return wrapper2


class BaseAccessor:
    def __init__(self, session=Depends(get_session)):
        self._session = session
