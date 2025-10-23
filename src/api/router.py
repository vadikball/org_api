from typing import Annotated
from fastapi import APIRouter, Depends, Query

from src.dependencies.base import BuildingServiceDependencyType, OrganizationServiceDependencyType
from src.middleware.api_token import get_api_key
from src.scheme.base import BuildingOut, OrganizationOut
from src.scheme.query_param import GeoListParam, OrganizationByCategoryListParam, OrganizationListParam, Page, PageParam


router = APIRouter(prefix="/v1", dependencies=[Depends(get_api_key)])


@router.get("/organizations")
async def get_organizations_page(
    service: OrganizationServiceDependencyType,
    query_param: Annotated[OrganizationListParam, Query()],
) -> Page[OrganizationOut]:
    """
    Get an organizations page by name or lon, lat, radius in query parameter.
    """

    return await service.get_page(query_param)


@router.get(
    "/organizations/{organization_id}",
    responses={
        404: {
            "description": "Organization not found",
            "content": {"application/json": {"example": {"detail": "Organization with id=123 not found."}}},
        }
    },
)
async def get_organization_detail(
    organization_id: int,
    service: OrganizationServiceDependencyType,
) -> OrganizationOut:
    """
    Get an organization by id.
    """

    return await service.get_by_id(organization_id)


@router.get("/buildings")
async def get_buildings_page(
    service: BuildingServiceDependencyType,
    query_param: Annotated[GeoListParam, Query()],
) -> Page[BuildingOut]:
    """
    Get a building page by lon, lat, radius in query parameter.
    """

    return await service.get_page(query_param)


@router.get("/buildings/{building_id}/organizations")
async def get_organizations_page_by_building(
    building_id: int,
    service: OrganizationServiceDependencyType,
    query_param: Annotated[PageParam, Query()],
) -> Page[OrganizationOut]:
    """
    Get an organization page by building id.
    """

    return await service.get_page_by_building(building_id, query_param)


@router.get("/categories/{category_id}/organizations")
async def get_organizations_page_by_category(
    category_id: int,
    service: OrganizationServiceDependencyType,
    query_param: Annotated[OrganizationByCategoryListParam, Query()],
) -> Page[OrganizationOut]:
    """
    Get an organization page by building id.
    """

    return await service.get_page_by_category(category_id, query_param)
