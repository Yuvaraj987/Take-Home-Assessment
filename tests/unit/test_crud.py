import pytest
from app.crud import create_repo, get_repo, update_repo
from app.models import Repository

@pytest.mark.asyncio
async def test_create_and_get_repo(db_session):
    repo_data = {
        "name": "fastapi",
        "owner": "tiangolo",
        "stars": 100,
        "description": "Test repo"
    }

    repo = await create_repo(db_session, repo_data)
    fetched = await get_repo(db_session, repo.id)

    assert fetched is not None
    assert fetched.name == "fastapi"
    assert fetched.owner == "tiangolo"


@pytest.mark.asyncio
async def test_update_repo(db_session):
    repo = Repository(
        name="fastapi",
        owner="tiangolo",
        stars=100,
        description="Old"
    )
    db_session.add(repo)
    await db_session.commit()
    await db_session.refresh(repo)

    updated = await update_repo(
        db_session,
        repo,
        {"stars": 500, "description": "Updated"}
    )

    assert updated.stars == 500
    assert updated.description == "Updated"
