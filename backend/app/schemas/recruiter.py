from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.schemas.auth import UserResponse
from app.schemas.company import CompanyResponse

class RecruiterResponse(BaseModel):
    id: str
    user_id: str
    company_id: str
    designation: Optional[str] = None
    created_at: datetime
    user: UserResponse
    company: CompanyResponse

    model_config = ConfigDict(from_attributes=True)
