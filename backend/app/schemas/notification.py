from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: str = Field(..., description="Target user ID")
    title: str = Field(..., min_length=1, max_length=255, description="Short notification title")
    message: str = Field(..., min_length=1, description="Notification body content")

class NotificationRead(BaseModel):
    id: str
    user_id: str
    title: str
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class NotificationUpdate(BaseModel):
    is_read: bool = True
