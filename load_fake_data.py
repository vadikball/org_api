import asyncio
from contextlib import asynccontextmanager

from loguru import logger

from src.dependencies.base import get_session
from src.lifespan.lifespan import lifespan
from src.service.fake_data import FakeDataService


async def load_data():
    async with lifespan():
        async with asynccontextmanager(get_session)() as session:
            faker_service = FakeDataService(session, logger)
            await faker_service.load()


def main():
    asyncio.run(load_data())


if __name__ == "main":
    main()
