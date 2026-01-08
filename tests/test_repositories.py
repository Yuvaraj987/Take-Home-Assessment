import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_repo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/repositories/",
            json={"owner": "tiangolo", "repo": "fastapi"}
        )
    assert response.status_code == 201
    assert "id" in response.json()

@pytest.mark.asyncio
async def test_get_invalid_repo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/repositories/9999")
    assert response.status_code == 404
