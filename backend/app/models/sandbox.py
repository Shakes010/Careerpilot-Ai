import uuid
import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Text, Integer, Float, DateTime, Enum, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class SandboxDifficulty(str, enum.Enum):
    BEGINNER = "BEGINNER"
    INTERMEDIATE = "INTERMEDIATE"
    ADVANCED = "ADVANCED"

class SandboxStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    PUBLISHED = "PUBLISHED"
    ARCHIVED = "ARCHIVED"

class AttemptStatus(str, enum.Enum):
    STARTED = "STARTED"
    SUBMITTED = "SUBMITTED"
    EVALUATED = "EVALUATED"

class SandboxChallenge(Base):
    __tablename__ = "sandbox_challenges"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    category = Column(String(100), nullable=False, default="Software Engineering")
    difficulty = Column(Enum(SandboxDifficulty), nullable=False, default=SandboxDifficulty.BEGINNER)
    skills = Column(String(512), nullable=True)
    instructions = Column(Text, nullable=False)
    time_limit = Column(Integer, nullable=True, help_text="Time limit in minutes")
    status = Column(Enum(SandboxStatus), nullable=False, default=SandboxStatus.PUBLISHED, index=True)
    created_by = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    creator = relationship("User", foreign_keys=[created_by])
    attempts = relationship("SandboxAttempt", back_populates="challenge", cascade="all, delete-orphan")

class SandboxAttempt(Base):
    __tablename__ = "sandbox_attempts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    challenge_id = Column(String(36), ForeignKey("sandbox_challenges.id", ondelete="CASCADE"), nullable=False, index=True)
    student_id = Column(String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    started_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    submitted_at = Column(DateTime, nullable=True)
    status = Column(Enum(AttemptStatus), nullable=False, default=AttemptStatus.STARTED, index=True)
    score = Column(Float, nullable=True)
    feedback = Column(Text, nullable=True)
    submission = Column(Text, nullable=True)

    challenge = relationship("SandboxChallenge", back_populates="attempts")
    student = relationship("User", foreign_keys=[student_id])
