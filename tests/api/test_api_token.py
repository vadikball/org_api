from httpx import AsyncClient

from src.core.settings import app_settings
from src.service.fake_data import FakeDataService


async def test_api_token(unauthorized_app_client: AsyncClient, lifespan_fake_data: FakeDataService) -> None:
    org_id = lifespan_fake_data.organizations[-1].id + 1
    response = await unauthorized_app_client.get(f"/organization_directory/v1/organizations/{org_id}")
    assert response.status_code == 401
    response = await unauthorized_app_client.get(
        f"/organization_directory/v1/organizations/{org_id}", headers={"X-API-Key": app_settings.API_TOKEN}
    )
    assert response.status_code == 404
