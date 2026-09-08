from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.sandbox import SandboxDifficulty, SandboxStatus, AttemptStatus

class ChallengeResponse(BaseModel):
    id: str
    title: str
    description: str
    category: str
    difficulty: SandboxDifficulty
    skills: Optional[str] = None
    instructions: str
    time_limit: Optional[int] = None
    status: SandboxStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class AttemptSubmitRequest(BaseModel):
    submission: str

class AttemptResponse(BaseModel):
    id: str
    challenge_id: str
    challenge_title: Optional[str] = ""
    student_id: str
    started_at: datetime
    submitted_at: Optional[datetime] = None
    status: AttemptStatus
    score: Optional[float] = None
    feedback: Optional[str] = None
    submission: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
