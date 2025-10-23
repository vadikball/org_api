from geoalchemy2.functions import ST_DWithin
from geoalchemy2.shape import from_shape, to_shape
from shapely import Point
from sqlalchemy import SQLColumnExpression

from src.db.models.models import BuildingModel


def building_to_lon_lat(building: BuildingModel) -> tuple[float, float]:
    """Return longitude, latitude of a given building."""
    point = to_shape(building.location)
    return point.x, point.y  # type: ignore


def radius_filter_function(lon: float, lat: float, radius: int) -> SQLColumnExpression:
    return ST_DWithin(BuildingModel.location, from_shape(Point(lon, lat), srid=4326), radius)
