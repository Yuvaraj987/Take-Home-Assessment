from fastapi import FastAPI
from app.database import engine, Base
from app.api.repositories import router as repo_router

app = FastAPI(title="FastAPI GitHub Repository Service")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(repo_router)
