from sqlalchemy import select
from src.db.models.models import BuildingModel
from src.repo.base import BaseRepo
from src.scheme.base import BuildingOut
from src.service.geo_shape import radius_filter_function


class BuildingRepo(BaseRepo[BuildingModel, BuildingOut]):
    model = BuildingModel

    async def get_list(
        self, lon: float | None, lat: float | None, radius: int | None, page: int, page_size: int
    ) -> list[BuildingOut]:
        filter_expressions = []
        if None not in {lat, lon, radius}:
            assert lat is not None and lon is not None and radius is not None
            filter_expressions.append(radius_filter_function(lon, lat, radius))

        limit, offset = self.page_to_limit_offset(page, page_size)

        query = select(self.model).where(*filter_expressions).limit(limit).offset(offset)

        buildings_from_db = (await self._session.execute(query)).scalars().all()

        return [self._to_domain(building_from_db) for building_from_db in buildings_from_db]

    def _to_domain(self, model_from_db: BuildingModel) -> BuildingOut:
        return BuildingOut(
            id=model_from_db.id,
            address=model_from_db.address,
            location=self._building_geo_point(model_from_db),
        )
