from abc import abstractmethod
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.models import BuildingModel, OrganizationModel
from src.scheme.base import GeometryPoint
from src.service.geo_shape import building_to_lon_lat


def page_to_limit_offset(page: int, page_size: int) -> tuple[int, int]:
    """Return tuple [limit, offset] from page parameters"""

    return page_size, page_size * (page - 1)


class BaseRepo[Model: BuildingModel | OrganizationModel, Scheme: BaseModel]:
    model: type[Model]

    def __init__(self, session: AsyncSession):
        self._session = session
        assert self.model is not None

    def page_to_limit_offset(self, page: int, page_size: int) -> tuple[int, int]:
        """Return tuple [limit, offset] from page parameters"""

        return page_size, page_size * (page - 1)

    def to_domain(self, organization_from_db: Model | None) -> Scheme | None:
        if organization_from_db is None:
            return None

        return self._to_domain(organization_from_db)

    @abstractmethod
    def _to_domain(self, model_from_db: Model) -> Scheme:
        raise NotImplementedError

    def _building_geo_point(self, building: BuildingModel) -> GeometryPoint:
        lon, lat = building_to_lon_lat(building)
        return GeometryPoint(coordinates=(lon, lat))
