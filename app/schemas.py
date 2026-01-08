from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class RepoCreate(BaseModel):
    owner: str = Field(..., min_length=1)
    repo: str = Field(..., min_length=1)

class RepoUpdate(BaseModel):
    description: Optional[str]
    stars: Optional[int] = Field(ge=0)

class RepoResponse(BaseModel):
    id: int
    name: str
    owner: str
    stars: int
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
