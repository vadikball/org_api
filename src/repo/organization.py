from sqlalchemy import SQLColumnExpression, select
from sqlalchemy.orm import aliased

from src.db.models.models import BuildingModel, CategoryModel, CategoryOrganizationModel, OrganizationModel
from src.repo.base import BaseRepo
from src.scheme.base import BuildingOut, CategoryOut, OrganizationOut
from src.service.geo_shape import radius_filter_function


class OrganizationRepo(BaseRepo[OrganizationModel, OrganizationOut]):
    model = OrganizationModel

    async def get_by_id(self, organization_id: int) -> OrganizationOut | None:
        query = select(OrganizationModel).where(OrganizationModel.id == organization_id)
        organization_from_db = (await self._session.execute(query)).scalar()

        return self.to_domain(organization_from_db)

    async def get_list(
        self, name: str | None, lon: float | None, lat: float | None, radius: int | None, page: int, page_size: int
    ) -> list[OrganizationOut]:
        filter_expressions = []
        join_building = False
        if name is not None:
            filter_expressions.append(OrganizationModel.name.ilike(f"%{name}%"))
        if None not in {lat, lon, radius}:
            assert lat is not None and lon is not None and radius is not None
            join_building = True
            filter_expressions.append(radius_filter_function(lon, lat, radius))

        return await self._get_list(filter_expressions, page, page_size, join_building=join_building)

    async def get_list_by_building(self, building_id: int, page: int, page_size: int) -> list[OrganizationOut]:
        return await self._get_list([OrganizationModel.building_id == building_id], page, page_size)

    async def get_list_by_category(
        self, category_id: int, page: int, page_size: int, include_subcategory: bool
    ) -> list[OrganizationOut]:
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

        return await self._get_list([filter_expression], page, page_size, True)

    async def _get_list(
        self,
        filter_expressions: list[SQLColumnExpression],
        page: int,
        page_size: int,
        join_category: bool = False,
        join_building: bool = False,
    ) -> list[OrganizationOut]:
        limit, offset = self.page_to_limit_offset(page, page_size)

        query = select(OrganizationModel)
        if join_category:
            query = query.join(
                CategoryOrganizationModel,
                OrganizationModel.id == CategoryOrganizationModel.organization_id,
            )
        if join_building:
            query = query.join(
                BuildingModel,
                OrganizationModel.building_id == BuildingModel.id,
            )

        query = query.where(*filter_expressions).limit(limit).offset(offset)

        organizations_from_db = (await self._session.execute(query)).scalars().all()

        return [self._to_domain(organization_from_db) for organization_from_db in organizations_from_db]

    def _to_domain(self, organization_from_db: OrganizationModel) -> OrganizationOut:
        building = None
        if organization_from_db.building is not None:
            building = BuildingOut(
                id=organization_from_db.building.id,
                address=organization_from_db.building.address,
                location=self._building_geo_point(organization_from_db.building),
            )

        return OrganizationOut(
            id=organization_from_db.id,
            name=organization_from_db.name,
            phone_number=organization_from_db.phone_number,
            building=building,
            categories=[CategoryOut.model_validate(category) for category in organization_from_db.categories],
        )
