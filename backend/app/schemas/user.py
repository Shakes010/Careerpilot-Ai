"""
user.py — Pydantic schemas for the User resource (admin-facing).

These schemas are deliberately minimal — they only expose the fields
needed by the User Management feature. Full auth/registration schemas
belong in the teammate's auth module.

Pydantic version: 1.10.x
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr


class UserRead(BaseModel):
    """Public-safe user representation returned by admin endpoints."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    full_name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime


class UserStatusUpdate(BaseModel):
    """
    Response model after toggling a user's active status.
    The PATCH endpoint doesn't need a request body — it just flips is_active.
    """

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    is_active: bool
    message: str
