from typing import Annotated

from pydantic import BaseModel, Field


class PageParam(BaseModel):
    page: Annotated[int, Field(strict=True, ge=1)] = 1
    page_size: Annotated[int, Field(strict=True, ge=1)] = 10


class OrganizationListParam(PageParam):
    name: str


class Page[PageData: BaseModel](BaseModel):
    page: Annotated[int, Field(strict=True, ge=1)]
    page_size: Annotated[int, Field(strict=True, ge=1)]
    page_data: list[PageData]
