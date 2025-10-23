from http import HTTPStatus
from typing import Annotated, AsyncGenerator

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import session
from src.repo.building import BuildingRepo
from src.repo.organization import OrganizationRepo
from src.service.building import BuildingService
from src.service.organization import OrganizationService


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    if session.session_factory_cache is None:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="impossible to create session")

    async with session.session_factory_cache() as db_session:
        try:
            yield db_session
        except Exception as exc:
            await db_session.rollback()
            raise exc


AsyncSessionDependencyType = Annotated[AsyncSession, Depends(get_session)]


def get_organization_repo(session: AsyncSessionDependencyType) -> OrganizationRepo:
    return OrganizationRepo(session)


OrganizationRepoDependencyType = Annotated[OrganizationRepo, Depends(get_organization_repo)]


def get_organization_service(organization_repo: OrganizationRepoDependencyType) -> OrganizationService:
    return OrganizationService(organization_repo)


OrganizationServiceDependencyType = Annotated[OrganizationService, Depends(get_organization_service)]


def get_building_repo(session: AsyncSessionDependencyType) -> BuildingRepo:
    return BuildingRepo(session)


BuildingRepoDependencyType = Annotated[BuildingRepo, Depends(get_building_repo)]


def get_building_service(building_repo: BuildingRepoDependencyType) -> BuildingService:
    return BuildingService(building_repo)


BuildingServiceDependencyType = Annotated[BuildingService, Depends(get_building_service)]
