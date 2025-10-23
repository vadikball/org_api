from http import HTTPStatus
from fastapi import HTTPException
from src.repo.organization import OrganizationRepo
from src.scheme.base import OrganizationOut
from src.scheme.query_param import OrganizationByCategoryListParam, OrganizationListParam, Page, PageParam


class OrganizationService:
    def __init__(self, organization_repo: OrganizationRepo):
        self._organization_repo = organization_repo

    async def get_by_id(self, organization_id: int) -> OrganizationOut:
        organization = await self._organization_repo.get_by_id(organization_id)
        if organization is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Organization not found.")

        return organization

    async def get_page(self, query_param: OrganizationListParam) -> Page[OrganizationOut]:
        organizations = await self._organization_repo.get_list(
            query_param.name, query_param.page, query_param.page_size
        )

        return Page[OrganizationOut](
            page=query_param.page,
            page_size=query_param.page_size,
            page_data=organizations,
        )

    async def get_page_by_building(self, building_id: int, query_param: PageParam) -> Page[OrganizationOut]:
        organizations = await self._organization_repo.get_list_by_building(
            building_id, query_param.page, query_param.page_size
        )

        return Page[OrganizationOut](
            page=query_param.page,
            page_size=query_param.page_size,
            page_data=organizations,
        )

    async def get_page_by_category(
        self, category_id: int, query_param: OrganizationByCategoryListParam
    ) -> Page[OrganizationOut]:
        organizations = await self._organization_repo.get_list_by_category(
            category_id, query_param.page, query_param.page_size, query_param.include_subcategories
        )

        return Page[OrganizationOut](
            page=query_param.page,
            page_size=query_param.page_size,
            page_data=organizations,
        )
