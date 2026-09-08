import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class FlagTargetType(str, enum.Enum):
    USER = "USER"
    JOB = "JOB"
    PROJECT = "PROJECT"
    COMMENT = "COMMENT"

class FlagStatus(str, enum.Enum):
    PENDING = "PENDING"
    WARNING_ISSUED = "WARNING_ISSUED"
    SUSPENDED = "SUSPENDED"
    DISMISSED = "DISMISSED"

class UserAudit(Base):
    __tablename__ = "user_audits"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    admin_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action = Column(String(100), nullable=False)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    admin = relationship("User", foreign_keys=[admin_id])

class FlaggedActivity(Base):
    __tablename__ = "flagged_activities"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    reporter_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    target_type = Column(Enum(FlagTargetType), nullable=False, default=FlagTargetType.USER)
    target_id = Column(String(36), nullable=False, index=True)
    reason = Column(Text, nullable=False)
    risk_score = Column(Float, nullable=False, default=50.0)
    status = Column(Enum(FlagStatus), nullable=False, default=FlagStatus.PENDING, index=True)
    resolved_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    reporter = relationship("User", foreign_keys=[reporter_id])
    resolver = relationship("User", foreign_keys=[resolved_by])

class PlatformTelemetry(Base):
    __tablename__ = "platform_telemetry"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    active_students = Column(Integer, nullable=False, default=0)
    active_recruiters = Column(Integer, nullable=False, default=0)
    total_jobs = Column(Integer, nullable=False, default=0)
    verified_companies = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
