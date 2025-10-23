from geoalchemy2 import WKBElement
from geoalchemy2.shape import to_shape
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.models import OrganizationModel
from src.scheme.base import BuildingOut, CategoryOut, GeometryPoint, OrganizationOut


class OrganizationRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, organization_id: int) -> OrganizationOut | None:
        query = select(OrganizationModel).where(OrganizationModel.id == organization_id)
        organization_from_db = (await self._session.execute(query)).scalar()

        return self.to_domain(organization_from_db)

    def to_domain(self, organization_from_db: OrganizationModel | None) -> OrganizationOut | None:
        if organization_from_db is None:
            return None

        return self._to_domain(organization_from_db)

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
