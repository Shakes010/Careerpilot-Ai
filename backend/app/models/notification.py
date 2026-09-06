"""
notification.py — Notification ORM model.

Table: notifications
  id          UUID PK
  user_id     UUID FK → users.id (cascade delete)
  title       VARCHAR(255)
  message     TEXT
  is_read     BOOLEAN  default false
  created_at  TIMESTAMPTZ  default now()

SQLAlchemy version: 1.4.x
"""

import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import text

from app.database import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        server_default=text("uuid_generate_v4()"),
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, nullable=False, default=False)
    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        server_default=text("now()"),
    )

    # ORM relationship back to User
    user = relationship(
        "User",
        back_populates="notifications",
    )

    def __repr__(self) -> str:
        return (
            f"<Notification id={self.id} user_id={self.user_id} "
            f"title={self.title!r} is_read={self.is_read}>"
        )
