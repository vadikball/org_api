from typing import AsyncIterator

import pytest
from asgi_lifespan import LifespanManager
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import app
from src.core.settings import app_settings
from src.db.models.models import BuildingModel, CategoryModel, CategoryOrganizationModel, OrganizationModel
from src.db.session import build_db_session_factory


@pytest.fixture
async def started_app() -> AsyncIterator[FastAPI]:
    async with LifespanManager(app) as manager:
        yield manager.app  # type: ignore


@pytest.fixture
async def app_client(started_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(
        transport=ASGITransport(app=started_app), base_url="http://test", headers={"X-API-Key": app_settings.API_TOKEN}
    ) as client:
        yield client


@pytest.fixture
async def unauthorized_app_client(started_app: FastAPI) -> AsyncIterator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=started_app), base_url="http://test") as client:
        yield client


@pytest.fixture
async def db_session() -> AsyncIterator[AsyncSession]:
    session_maker = await build_db_session_factory()
    async with session_maker() as session:
        try:
            await session.execute(delete(CategoryOrganizationModel))
            await session.execute(delete(OrganizationModel))
            await session.execute(delete(BuildingModel))
            await session.execute(delete(CategoryModel))
            yield session
        except Exception as e:
            await session.rollback()
            raise e
