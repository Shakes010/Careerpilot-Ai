from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.notification import Notification
from app.models.user import User
from app.schemas.auth import ApiResponse
from app.schemas.notification import NotificationCreate, NotificationRead, NotificationUpdate
from app.repositories.notification_repository import NotificationRepository
from app.repositories.user_repository import UserRepository
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/notifications", tags=["Notification Management"])

@router.post("/", response_model=ApiResponse[NotificationRead], status_code=status.HTTP_201_CREATED)
def send_notification(payload: NotificationCreate, db: Session = Depends(get_db)):
    """Send / create a new notification for a target user."""
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(payload.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Target user with ID {payload.user_id} not found."
        )

    repo = NotificationRepository(db)
    notification = Notification(
        user_id=payload.user_id,
        title=payload.title,
        message=payload.message
    )
    created = repo.create(notification)
    return ApiResponse(
        success=True,
        data=NotificationRead.model_validate(created),
        message="Notification sent successfully."
    )

@router.get("/user/{user_id}", response_model=ApiResponse[List[NotificationRead]])
def list_user_notifications(user_id: str, db: Session = Depends(get_db)):
    """List all notifications for a specific user (newest first)."""
    user_repo = UserRepository(db)
    user = user_repo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found."
        )

    repo = NotificationRepository(db)
    notifications = repo.get_by_user_id(user_id)
    return ApiResponse(
        success=True,
        data=[NotificationRead.model_validate(n) for n in notifications],
        message="Notifications retrieved."
    )

@router.get("/me", response_model=ApiResponse[dict])
def get_my_notifications(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Retrieve notifications and unread count for the currently logged-in user."""
    repo = NotificationRepository(db)
    notifications = repo.get_by_user_id(user.id)
    unread_count = repo.get_unread_count(user.id)
    return ApiResponse(
        success=True,
        data={
            "notifications": [NotificationRead.model_validate(n) for n in notifications],
            "unread_count": unread_count
        },
        message="My notifications retrieved."
    )

@router.patch("/{notification_id}/read", response_model=ApiResponse[NotificationRead])
def mark_notification_as_read(
    notification_id: str,
    payload: NotificationUpdate = NotificationUpdate(),
    db: Session = Depends(get_db)
):
    """Mark a specific notification as read."""
    repo = NotificationRepository(db)
    updated = repo.mark_as_read(notification_id, payload.is_read)
    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Notification with ID {notification_id} not found."
        )
    return ApiResponse(
        success=True,
        data=NotificationRead.model_validate(updated),
        message="Notification marked as read."
    )
