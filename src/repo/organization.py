from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy import SQLColumnExpression, select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.models import CategoryModel, CategoryOrganizationModel, OrganizationModel
from src.scheme.base import BuildingOut, CategoryOut, GeometryPoint, OrganizationOut


def page_to_limit_offset(page: int, page_size: int) -> tuple[int, int]:
    """Return tuple [limit, offset] from page parameters"""

    return page_size, page_size * (page - 1)


class OrganizationRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, organization_id: int) -> OrganizationOut | None:
        query = select(OrganizationModel).where(OrganizationModel.id == organization_id)
        organization_from_db = (await self._session.execute(query)).scalar()

        return self.to_domain(organization_from_db)

    async def get_list(self, name: str, page: int, page_size: int) -> list[OrganizationOut]:
        return await self._get_list(OrganizationModel.name.ilike(f"%{name}%"), page, page_size)

    async def get_list_by_building(self, building_id: int, page: int, page_size: int) -> list[OrganizationOut]:
        return await self._get_list(OrganizationModel.building_id == building_id, page, page_size)

    async def get_list_by_category(
        self, category_id: int, page: int, page_size: int, include_subcategory: bool
    ) -> list[OrganizationOut]:
        limit, offset = page_to_limit_offset(page, page_size)
        filter_expression = CategoryOrganizationModel.category_id == category_id
        if include_subcategory:
            base = select(CategoryModel.id, CategoryModel.parent_id).where(CategoryModel.id == category_id)

            recursive = select(CategoryModel.id, CategoryModel.parent_id).join(
                base.cte(name="category_tree", recursive=True),
                CategoryModel.parent_id == base.c.id,
            )

            category_tree = base.cte(name="category_tree", recursive=True)
            category_tree = category_tree.union_all(recursive)

            c1 = aliased(CategoryModel)
            c2 = aliased(CategoryModel)
            c3 = aliased(CategoryModel)

            subq = (
                select(c1.id)
                .where(c1.id == category_id)
                .union_all(
                    select(c2.id).where(c2.parent_id == c1.id),
                    select(c3.id).where(c3.parent_id == c2.id),
                )
                .subquery()
            )
            filter_expression = CategoryOrganizationModel.category_id.in_(select(subq.c.id))

        query = (
            select(OrganizationModel)
            .join(
                CategoryOrganizationModel,
                OrganizationModel.id == CategoryOrganizationModel.organization_id,
            )
            .where(filter_expression)
            .limit(limit)
            .offset(offset)
        )
        organizations_from_db = (await self._session.execute(query)).scalars().all()

        return [self._to_domain(organization_from_db) for organization_from_db in organizations_from_db]

    def to_domain(self, organization_from_db: OrganizationModel | None) -> OrganizationOut | None:
        if organization_from_db is None:
            return None

        return self._to_domain(organization_from_db)

    async def _get_list(
        self, filter_expression: SQLColumnExpression, page: int, page_size: int
    ) -> list[OrganizationOut]:
        limit, offset = page_to_limit_offset(page, page_size)
        query = select(OrganizationModel).where(filter_expression).limit(limit).offset(offset)
        organizations_from_db = (await self._session.execute(query)).scalars().all()

        return [self._to_domain(organization_from_db) for organization_from_db in organizations_from_db]

    def _to_domain(self, organization_from_db: OrganizationModel) -> OrganizationOut:
        building = None
        if organization_from_db.building is not None:
            building = BuildingOut(
                id=organization_from_db.building.id,
                address=organization_from_db.building.address,
                location=self.__building_geo_point(organization_from_db.building.location),
            )

        return OrganizationOut(
            id=organization_from_db.id,
            name=organization_from_db.name,
            phone_number=organization_from_db.phone_number,
            building=building,
            categories=[CategoryOut.model_validate(category) for category in organization_from_db.categories],
        )

    def __building_geo_point(self, location: WKBElement) -> GeometryPoint:
        point = to_shape(location)
        return GeometryPoint(coordinates=(point.x, point.y))  # type: ignore
