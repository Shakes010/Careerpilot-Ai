from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.notification import Notification

class NotificationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, notification: Notification) -> Notification:
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_by_id(self, notification_id: str) -> Optional[Notification]:
        return self.db.query(Notification).filter(Notification.id == notification_id).first()

    def get_by_user_id(self, user_id: str, limit: int = 100) -> List[Notification]:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .order_by(Notification.created_at.desc())
            .limit(limit)
            .all()
        )

    def mark_as_read(self, notification_id: str, is_read: bool = True) -> Optional[Notification]:
        notification = self.get_by_id(notification_id)
        if not notification:
            return None
        notification.is_read = is_read
        self.db.commit()
        self.db.refresh(notification)
        return notification

    def get_unread_count(self, user_id: str) -> int:
        return (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id, Notification.is_read == False)
            .count()
        )
