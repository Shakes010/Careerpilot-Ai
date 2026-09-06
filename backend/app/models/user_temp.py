# =============================================================================
# TEMPORARY - replace with real users model once teammate pushes their auth
# module. Do not build additional logic assuming this is final.
# =============================================================================
"""
user_temp.py — Minimal User reference model.

This model exists solely so that:
  - notifications.user_id FK can resolve at SQLAlchemy mapping time.
  - The admin User-Management routes have a table to query.

It intentionally mirrors ONLY the columns needed by the Recruiter /
Payment / Notification modules. Once the real auth module lands, delete
this file and update imports throughout this package.

SQLAlchemy version: 1.4.x
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    role = Column(
        String(50),
        nullable=False,
        default="student",
        comment="One of: student | recruiter | admin",
    )
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
    )

    # Relationship — allows notification.user to be accessed ORM-side.
    notifications = relationship(
        "Notification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} email={self.email!r} role={self.role!r}>"
