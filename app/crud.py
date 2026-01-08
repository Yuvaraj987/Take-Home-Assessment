from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .models import Repository

async def create_repo(db: AsyncSession, repo_data: dict):
    repo = Repository(**repo_data)
    db.add(repo)
    await db.commit()
    await db.refresh(repo)
    return repo

async def get_repo(db: AsyncSession, repo_id: int):
    result = await db.execute(select(Repository).where(Repository.id == repo_id))
    return result.scalar_one_or_none()

async def update_repo(db: AsyncSession, repo: Repository, updates: dict):
    for key, value in updates.items():
        setattr(repo, key, value)
    await db.commit()
    await db.refresh(repo)
    return repo

async def delete_repo(db: AsyncSession, repo: Repository):
    await db.delete(repo)
    await db.commit()
