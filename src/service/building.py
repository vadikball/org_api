from src.repo.building import BuildingRepo
from src.scheme.base import BuildingOut
from src.scheme.query_param import GeoListParam, Page


class BuildingService:
    def __init__(self, building_repo: BuildingRepo):
        self._building_repo = building_repo

    async def get_page(self, query_param: GeoListParam) -> Page[BuildingOut]:
        buildings = await self._building_repo.get_list(
            query_param.lon,
            query_param.lat,
            query_param.radius,
            query_param.page,
            query_param.page_size,
        )

        return Page[BuildingOut](
            page=query_param.page,
            page_size=query_param.page_size,
            page_data=buildings,
        )
