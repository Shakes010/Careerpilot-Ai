from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional, Generic, TypeVar, Any

T = TypeVar('T')

class ApiResponse(BaseModel, Generic[T]):
    success: bool = True
    data: Optional[T] = None
    message: str = "Operation successful"
    error_code: Optional[str] = None

class RecruiterRegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=100)
    phone: Optional[str] = None
    designation: Optional[str] = "Hiring Manager"
    company_name: str = Field(..., min_length=2, max_length=150)
    company_website: Optional[str] = None

class RecruiterLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    email: str
    full_name: str
    role: str
    company_id: str
    company_name: str
    company_verification_status: str

class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    role: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
