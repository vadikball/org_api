from typing import Optional

from geoalchemy2 import Geography, WKBElement
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

from src.db.base import Base


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=True)


class BuildingModel(Base):
    __tablename__ = "buildings"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    address: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[WKBElement] = mapped_column(
        Geography("POINT", srid=4326),
    )


class OrganizationModel(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    phone_number: Mapped[Optional[list[str]]] = mapped_column(ARRAY(String))
    building_id: Mapped[int] = mapped_column(ForeignKey(BuildingModel.id, ondelete="SET NULL"))

    building: Mapped[Optional[BuildingModel]] = relationship(lazy="selectin")
    categories: Mapped[list[CategoryModel]] = relationship(secondary="category_organization", lazy="selectin")


class CategoryOrganizationModel(Base):
    __tablename__ = "category_organization"

    category_id: Mapped[int] = mapped_column(ForeignKey(CategoryModel.id), primary_key=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey(OrganizationModel.id), primary_key=True)
