import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas import RepoCreate, RepoUpdate, RepoResponse
from app.crud import create_repo, get_repo, update_repo, delete_repo

router = APIRouter(prefix="/repositories", tags=["Repositories"])

GITHUB_API = "https://github.com/Yuvaraj987/Take-Home-Assessment.git"

# 1️⃣ POST
@router.post("/", response_model=RepoResponse, status_code=status.HTTP_201_CREATED)
async def create_repository(payload: RepoCreate, db: AsyncSession = Depends(get_db)):
    url = f"{GITHUB_API}/{payload.owner}/{payload.repo}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=404, detail="GitHub repository not found")

    data = response.json()

    repo_data = {
        "name": data["name"],
        "owner": data["owner"]["login"],
        "stars": data["stargazers_count"],
        "description": data.get("description"),
    }

    return await create_repo(db, repo_data)

# 2️⃣ GET
@router.get("/{repo_id}", response_model=RepoResponse)
async def read_repository(repo_id: int, db: AsyncSession = Depends(get_db)):
    repo = await get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo

# 3️⃣ PUT
@router.put("/{repo_id}", response_model=RepoResponse)
async def update_repository(
    repo_id: int, payload: RepoUpdate, db: AsyncSession = Depends(get_db)
):
    repo = await get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    updates = payload.dict(exclude_unset=True)
    return await update_repo(db, repo, updates)

# 4️⃣ DELETE
@router.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_repository(repo_id: int, db: AsyncSession = Depends(get_db)):
    repo = await get_repo(db, repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")

    await delete_repo(db, repo)
