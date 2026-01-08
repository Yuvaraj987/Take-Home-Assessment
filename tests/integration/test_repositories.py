import pytest
from httpx import AsyncClient
from app.main import app

MOCK_GITHUB_RESPONSE = {
    "name": "fastapi",
    "owner": {"login": "tiangolo"},
    "stargazers_count": 999,
    "description": "Mocked GitHub repo"
}

@pytest.mark.asyncio
async def test_create_repository_api(override_db, monkeypatch):

    async def mock_github_get(self, url):
        class MockResponse:
            status_code = 200
            def json(self):
                return MOCK_GITHUB_RESPONSE
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_github_get)

    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "/repositories/",
            json={"owner": "tiangolo", "repo": "fastapi"}
        )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "fastapi"
    assert body["stars"] == 999


@pytest.mark.asyncio
async def test_get_repository_not_found(override_db):
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/repositories/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_repository(override_db, monkeypatch):

    async def mock_github_get(self, url):
        class MockResponse:
            status_code = 200
            def json(self):
                return MOCK_GITHUB_RESPONSE
        return MockResponse()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_github_get)

    async with AsyncClient(app=app, base_url="http://test") as client:
        create = await client.post(
            "/repositories/",
            json={"owner": "tiangolo", "repo": "fastapi"}
        )
        repo_id = create.json()["id"]

        delete = await client.delete(f"/repositories/{repo_id}")
        get_again = await client.get(f"/repositories/{repo_id}")

    assert delete.status_code == 204
    assert get_again.status_code == 404
