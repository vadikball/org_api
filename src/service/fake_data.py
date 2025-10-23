import random

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from geoalchemy2.shape import from_shape
from shapely.geometry import Point

from src.core.logger import LoggerBase
from src.db.models.models import (
    CategoryModel,
    BuildingModel,
    OrganizationModel,
    CategoryOrganizationModel,
)

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from loguru import Logger


class FakeDataService(LoggerBase):
    """Service to load fake data into storage."""

    def __init__(self, session: AsyncSession, simple_logger: "Logger") -> None:
        super().__init__(simple_logger)

        self._session = session
        self._faker = Faker("en_US")
        self.categories = []
        self.buildings = []
        self.organizations = []

    async def load(self):
        """Load fake categories, buildings, and organizations."""

        # Avoid duplicate seeding
        existing = await self._session.scalar(select(OrganizationModel.id).limit(1))
        if existing:
            self.logger.info("Fake data already loaded.")
            return

        self.logger.info("Generating fake data...")

        # 1. Create categories
        food = CategoryModel(name="Food")
        auto = CategoryModel(name="Automobiles")
        self._session.add_all([food, auto])
        await self._session.flush()  # get IDs assigned

        meat = CategoryModel(name="Meat Products", parent_id=food.id)
        dairy = CategoryModel(name="Dairy Products", parent_id=food.id)

        trucks = CategoryModel(name="Trucks", parent_id=auto.id)
        cars = CategoryModel(name="Cars", parent_id=auto.id)
        accessories = CategoryModel(name="Accessories", parent_id=auto.id)

        self._session.add_all([meat, dairy, trucks, cars, accessories])
        await self._session.flush()  # get IDs assigned

        # 2. Create random buildings
        for _ in range(10):
            lat = random.uniform(55.5, 55.9)  # example: around Moscow
            lon = random.uniform(37.3, 37.9)
            point = from_shape(Point(lon, lat), srid=4326)

            building = BuildingModel(
                address=self._faker.address(),
                location=point,
            )
            self.buildings.append(building)
        self._session.add_all(self.buildings)
        await self._session.flush()

        # 3. Create organizations
        self.categories = [food, meat, dairy, auto, trucks, cars, accessories]

        for _ in range(20):
            org = OrganizationModel(
                name=self._faker.company(),
                phone_number=[self._faker.phone_number() for _ in range(random.randint(1, 3))],
                building_id=random.choice(self.buildings).id,
            )
            self.organizations.append(org)
        self._session.add_all(self.organizations)
        await self._session.flush()

        # 4. Link orgs to random categories
        for org in self.organizations:
            for cat in random.sample(self.categories, random.randint(1, 2)):
                self._session.add(CategoryOrganizationModel(category_id=cat.id, organization_id=org.id))

        # 5. Commit all data
        await self._session.commit()
        self.logger.info("✅ Fake data successfully loaded.")
