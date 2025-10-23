from httpx import AsyncClient

from src.scheme.base import OrganizationOut
from src.service.fake_data import FakeDataService


async def test_organization_id(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]

    response = await app_client.get(f"/organization_directory/v1/organizations/{org.id}")
    response_model = OrganizationOut(**response.json())

    assert response_model.id == org.id
    assert response_model.building
    assert response_model.building.id == org.building.id
    assert response_model.categories
