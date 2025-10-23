from http import HTTPStatus
from fastapi import HTTPException
from src.repo.organization import OrganizationRepo
from src.scheme.base import OrganizationOut


class OrganizationService:
    def __init__(self, organization_repo: OrganizationRepo):
        self._organization_repo = organization_repo

    async def get_by_id(self, organization_id: int) -> OrganizationOut:
        organization = await self._organization_repo.get_by_id(organization_id)
        if organization is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Organization not found.")

        return organization
