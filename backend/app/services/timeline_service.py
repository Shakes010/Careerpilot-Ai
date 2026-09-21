from datetime import datetime
from sqlalchemy.orm import Session
from app.models.student import StudentTimelineEvent

def log_timeline_event(
    db: Session,
    student_id: int,
    title: str,
    description: str,
    category: str = "Milestone"
) -> StudentTimelineEvent:
    """
    Helper function to record a career development event in student_timeline_events table.
    """
    event = StudentTimelineEvent(
        student_id=student_id,
        title=title,
        description=description,
        category=category,
        event_date=datetime.utcnow()
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
