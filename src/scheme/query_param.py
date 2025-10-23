from typing import Annotated, Self

from pydantic import BaseModel, Field, model_validator


class PageParam(BaseModel):
    page: Annotated[int, Field(ge=1)] = 1
    page_size: Annotated[int, Field(ge=1)] = 10


class GeoListParam(PageParam):
    lon: float | None = None
    lat: float | None = None
    radius: int | None = None

    @property
    def geo_values(self) -> tuple[float | None, float | None, int | None]:
        return self.lon, self.lat, self.radius

    @model_validator(mode="after")
    def check_passwords_match(self) -> Self:
        if all(geo_value is None for geo_value in self.geo_values):
            return self

        if all(geo_value is not None for geo_value in self.geo_values):
            return self

        value_names = ["longitude", "latitude", "radius"]
        not_provided_values = [
            value_names[index] for index, geo_value in enumerate(self.geo_values) if geo_value is None
        ]
        raise ValueError(f"Incomplete values to execute geo search. Missed values: {', '.join(not_provided_values)}")


class OrganizationListParam(GeoListParam):
    name: str | None = None


class OrganizationByCategoryListParam(PageParam):
    include_subcategories: bool = False


class Page[PageData: BaseModel](BaseModel):
    page: Annotated[int, Field(ge=1)]
    page_size: Annotated[int, Field(ge=1)]
    page_data: list[PageData]
