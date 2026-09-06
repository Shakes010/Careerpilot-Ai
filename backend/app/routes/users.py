"""
users.py — FastAPI router for the User Management feature (admin-facing).

Endpoints:
  GET    /users/                           List all users
  GET    /users/{user_id}                  Get a single user by ID
  PATCH  /users/{user_id}/toggle-status    Suspend or activate a user (toggles is_active)
"""

import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_temp import User
from app.schemas.user import UserRead, UserStatusUpdate

router = APIRouter(
    prefix="/users",
    tags=["User Management"],
)


# ---------------------------------------------------------------------------
# GET /users/  — List all users
# ---------------------------------------------------------------------------
@router.get(
    "/",
    response_model=List[UserRead],
    summary="List all users (admin)",
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[User]:
    """
    Returns a paginated list of all users.
    - `skip`  — number of records to skip (for pagination)
    - `limit` — maximum records to return (max 100 per request)
    """
    return db.query(User).offset(skip).limit(min(limit, 100)).all()


# ---------------------------------------------------------------------------
# GET /users/{user_id}  — Get a single user
# ---------------------------------------------------------------------------
@router.get(
    "/{user_id}",
    response_model=UserRead,
    summary="Get a single user by UUID (admin)",
)
def get_user(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> User:
    """Returns the user with the given UUID, or 404 if not found."""
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return user


# ---------------------------------------------------------------------------
# PATCH /users/{user_id}/toggle-status  — Suspend / activate
# ---------------------------------------------------------------------------
@router.patch(
    "/{user_id}/toggle-status",
    response_model=UserStatusUpdate,
    summary="Toggle a user's active status (suspend / activate)",
)
def toggle_user_status(
    user_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> UserStatusUpdate:
    """
    Flips `is_active` for the given user:
      - True  → False  (suspend)
      - False → True   (activate)

    Returns the new status and a human-readable message.
    """
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )

    user.is_active = not user.is_active
    db.commit()
    db.refresh(user)

    action = "activated" if user.is_active else "suspended"
    return UserStatusUpdate(
        id=user.id,
        is_active=user.is_active,
        message=f"User {user.email} has been {action} successfully.",
    )
