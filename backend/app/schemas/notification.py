"""
notification.py — Pydantic schemas for the Notification resource.

Request / response contracts for:
  - NotificationCreate  (POST /notifications/)
  - NotificationRead    (GET  /notifications/{user_id}, response model)
  - NotificationUpdate  (PATCH /notifications/{id}/read, request body)

Pydantic version: 1.10.x
"""

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NotificationCreate(BaseModel):
    """Payload for creating (sending) a new notification."""

    user_id: uuid.UUID = Field(..., description="UUID of the target user")
    title: str = Field(..., min_length=1, max_length=255, description="Short notification title")
    message: str = Field(..., min_length=1, description="Full notification body text")


class NotificationRead(BaseModel):
    """Full notification representation returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    message: str
    is_read: bool
    created_at: datetime


class NotificationUpdate(BaseModel):
    """
    Body for marking a notification as read.
    Only is_read is patchable through this endpoint.
    """

    is_read: bool = True
