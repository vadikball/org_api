from httpx import AsyncClient

from src.scheme.base import OrganizationOut
from src.scheme.query_param import Page
from src.service.fake_data import FakeDataService


async def test_organizations_name(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]

    response = await app_client.get("/organization_directory/v1/organizations", params={"name": org.name})
    response_model = Page[OrganizationOut](**response.json())

    assert response_model.page_data[0].id == org.id


async def test_organizations_building(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]

    response = await app_client.get(f"/organization_directory/v1/buildings/{org.building_id}/organizations")
    response_model = Page[OrganizationOut](**response.json())
    response_org = [org_from_api for org_from_api in response_model.page_data if org_from_api.id == org.id]
    assert response_org


async def test_organizations_category(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    # check up to 3 category deep constraint!

    food_category = lifespan_fake_data.categories[0]

    organizations = lifespan_fake_data.organizations
    chicken_org = organizations[-1]

    response = await app_client.get(f"/organization_directory/v1/categories/{food_category.id}/organizations")
    response_model = Page[OrganizationOut](**response.json())
    assert response.status_code == 200
    for org_from_api in response_model.page_data:
        assert food_category.id in {category.id for category in org_from_api.categories}

    response = await app_client.get(
        f"/organization_directory/v1/categories/{food_category.id}/organizations", params={"include_subcategory": True}
    )
    response_model = Page[OrganizationOut](**response.json())
    assert response.status_code == 200
    for org_from_api in response_model.page_data:
        assert chicken_org.id not in {category.id for category in org_from_api.categories}


async def test_organization_id(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]

    response = await app_client.get(f"/organization_directory/v1/organizations/{org.id}")
    response_model = OrganizationOut(**response.json())

    assert response_model.id == org.id
    assert response_model.building is not None and response_model.building.id == org.building.id
    assert response_model.categories
