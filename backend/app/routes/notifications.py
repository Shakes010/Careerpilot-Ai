"""
notifications.py — FastAPI router for the Notification Management feature.

Endpoints:
  POST   /notifications/                          Send a notification to a user
  GET    /notifications/user/{user_id}            List all notifications for a user
  PATCH  /notifications/{notification_id}/read    Mark a notification as read
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.notification import Notification
from app.models.user_temp import User
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


# ---------------------------------------------------------------------------
# POST /notifications/  — Send / create a notification
# ---------------------------------------------------------------------------
@router.post(
    "/",
    response_model=NotificationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Send a notification to a user",
)
def send_notification(
    payload: NotificationCreate,
    db: Session = Depends(get_db),
) -> Notification:
    """
    Create and persist a new notification for the given user.
    Returns 404 if the target user does not exist.
    """
    user = db.query(User).get(payload.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {payload.user_id} not found",
        )

    notification = Notification(
        user_id=payload.user_id,
        title=payload.title,
        message=payload.message,
    )
    db.add(notification)
    db.commit()
    db.refresh(notification)
    return notification


# ---------------------------------------------------------------------------
# GET /notifications/user/{user_id}  — List notifications for a user
# ---------------------------------------------------------------------------
@router.get(
    "/user/{user_id}",
    response_model=List[NotificationRead],
    summary="List all notifications for a user (newest first)",
)
def list_notifications(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> List[Notification]:
    """
    Returns all notifications for the given user, sorted newest-first.
    Returns 404 if the user doesn't exist.
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )

    notifications = (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )
    return notifications


# ---------------------------------------------------------------------------
# PATCH /notifications/{notification_id}/read  — Mark as read
# ---------------------------------------------------------------------------
@router.patch(
    "/{notification_id}/read",
    response_model=NotificationRead,
    summary="Mark a notification as read",
)
def mark_as_read(
    notification_id: uuid.UUID,
    payload: NotificationUpdate = NotificationUpdate(),
    db: Session = Depends(get_db),
) -> Notification:
    """
    Sets is_read = True (or the value provided in the request body)
    on the specified notification.
    Returns 404 if the notification doesn't exist.
    """
    notification = db.query(Notification).get(notification_id)
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification {notification_id} not found",
        )

    notification.is_read = payload.is_read
    db.commit()
    db.refresh(notification)
    return notification
