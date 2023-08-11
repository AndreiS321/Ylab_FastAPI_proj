from abc import ABC

from fastapi import Depends

from db import get_session


class BaseAccessor(ABC):
    def __init__(self, session=Depends(get_session)):
        self._session = session
