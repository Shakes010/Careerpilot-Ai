from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class SkillCreateRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    category: str = Field(default="General", min_length=2, max_length=100)
    description: Optional[str] = None

class SkillUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    description: Optional[str] = None

class SkillResponse(BaseModel):
    id: str
    name: str
    category: str
    description: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
