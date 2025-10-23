from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from src.db import session


@asynccontextmanager
async def lifespan() -> AsyncIterator[None]:
    session.session_factory_cache = await session.build_db_session_factory()
    yield
    await session.close_db_connections()


@asynccontextmanager
async def app_lifespan(app: FastAPI) -> AsyncIterator[None]:
    async with lifespan():
        yield
