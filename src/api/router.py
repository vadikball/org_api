from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.dependencies.base import OrganizationServiceDependencyType
from src.middleware.api_token import get_api_key
from src.scheme.base import OrganizationOut
from src.scheme.query_param import OrganizationListParam, Page, PageParam


router = APIRouter(prefix="/v1", dependencies=[Depends(get_api_key)])


@router.get("/organizations")
async def get_organizations_list(
    service: OrganizationServiceDependencyType,
    query_param: Annotated[OrganizationListParam, Query()],
) -> Page[OrganizationOut]:
    """
    Get an organizations page by name in query parameter.
    """

    return await service.get_page(query_param)


@router.get("/organizations/{organization_id}")
async def get_organization_detail(
    organization_id: int,
    service: OrganizationServiceDependencyType,
) -> OrganizationOut:
    """
    Get an organization by id.
    """

    return await service.get_by_id(organization_id)


@router.get("/buildings/{building_id}/organizations")
async def get_organizations_from_building(
    building_id: int,
    service: OrganizationServiceDependencyType,
    query_param: Annotated[PageParam, Query()],
) -> Page[OrganizationOut]:
    """
    Get an organization page by building id.
    """

    return await service.get_page_by_building(building_id, query_param)
