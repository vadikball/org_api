from fastapi import APIRouter, Depends

from src.dependencies.base import OrganizationServiceDependencyType
from src.middleware.api_token import get_api_key
from src.scheme.base import OrganizationOut


router = APIRouter(prefix="/v1", dependencies=[Depends(get_api_key)])


@router.get("/organizations/{organization_id}")
async def get_organization_detail(
    organization_id: int,
    service: OrganizationServiceDependencyType,
) -> OrganizationOut:
    """
    Get an organization by id.
    """

    return await service.get_by_id(organization_id)
