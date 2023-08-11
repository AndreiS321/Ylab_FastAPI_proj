from fastapi import Depends

from crud.routers import router_common as router
from crud_db.common import CommonAccessor


@router.get('/')
async def get_objects_list(accessor: CommonAccessor = Depends(CommonAccessor)):
    return await accessor.get_list()
