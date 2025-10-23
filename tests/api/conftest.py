from typing import AsyncIterator

from loguru import logger
import pytest
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.service.fake_data import FakeDataService
from src.db.models.models import (
    CategoryModel,
    BuildingModel,
    OrganizationModel,
    CategoryOrganizationModel,
)


@pytest.fixture
def faker_service(db_session: AsyncSession) -> FakeDataService:
    return FakeDataService(db_session, logger)


@pytest.fixture
async def clean_up_fake_data(db_session: AsyncSession) -> AsyncIterator[None]:
    yield
    await db_session.execute(delete(CategoryOrganizationModel))
    await db_session.execute(delete(OrganizationModel))
    await db_session.execute(delete(BuildingModel))
    await db_session.execute(delete(CategoryModel))


@pytest.fixture
async def insert_fake_data(faker_service: FakeDataService) -> FakeDataService:
    await faker_service.load()
    return faker_service


@pytest.fixture
async def lifespan_fake_data(
    insert_fake_data: FakeDataService, clean_up_fake_data: None
) -> AsyncIterator[FakeDataService]:
    yield insert_fake_data
