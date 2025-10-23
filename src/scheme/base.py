from typing import Literal

from pydantic import BaseModel


class GeometryPoint(BaseModel):
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float]  # (longitude, latitude)


class BaseFromAttrs(BaseModel):
    model_config = {"from_attributes": True}


class CategoryOut(BaseFromAttrs):
    id: int
    name: str


class BuildingOut(BaseFromAttrs):
    id: int
    address: str
    location: GeometryPoint


class OrganizationOut(BaseFromAttrs):
    id: int
    name: str
    phone_number: list[str] | None

    building: BuildingOut | None
    categories: list[CategoryOut] = []
