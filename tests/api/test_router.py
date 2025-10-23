from httpx import AsyncClient

from src.scheme.base import BuildingOut, OrganizationOut
from src.scheme.query_param import Page
from src.service.fake_data import FakeDataService
from src.service.geo_shape import building_to_lon_lat


async def test_organizations_name(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]

    response = await app_client.get("/organization_directory/v1/organizations", params={"name": org.name})
    response_model = Page[OrganizationOut](**response.json())

    assert response_model.page_data[0].id == org.id


async def test_organizations_geo(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]
    building = org.building
    assert building is not None
    lon, lat = building_to_lon_lat(building)

    response = await app_client.get(
        "/organization_directory/v1/organizations", params={"lon": lon, "lat": lat, "radius": 500, "page_size": 20}
    )
    response_model = Page[OrganizationOut](**response.json())

    assert [org_from_api for org_from_api in response_model.page_data if org_from_api.id == org.id]

    response = await app_client.get(
        "/organization_directory/v1/organizations", params={"lon": lon, "lat": lat, "radius": None}
    )
    assert response.status_code == 422


async def test_buildings_geo(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    buildings = lifespan_fake_data.buildings
    building = buildings[0]
    lon, lat = building_to_lon_lat(building)

    response = await app_client.get(
        "/organization_directory/v1/buildings", params={"lon": lon, "lat": lat, "radius": 500}
    )
    response_model = Page[BuildingOut](**response.json())

    assert [building_from_api for building_from_api in response_model.page_data if building_from_api.id == building.id]

    response = await app_client.get(
        "/organization_directory/v1/buildings", params={"lon": lon, "lat": lat, "radius": None}
    )
    assert response.status_code == 422


async def test_organizations_building(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    organizations = lifespan_fake_data.organizations
    org = organizations[0]

    response = await app_client.get(f"/organization_directory/v1/buildings/{org.building_id}/organizations")
    response_model = Page[OrganizationOut](**response.json())
    response_org = [org_from_api for org_from_api in response_model.page_data if org_from_api.id == org.id]
    assert response_org


async def test_organizations_category(app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
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
