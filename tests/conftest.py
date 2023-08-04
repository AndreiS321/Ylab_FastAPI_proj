from .fixtures import *


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"
