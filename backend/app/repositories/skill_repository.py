from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.skill import Skill

class SkillRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, skill_id: str) -> Optional[Skill]:
        return self.db.query(Skill).filter(Skill.id == skill_id).first()

    def get_by_name(self, name: str) -> Optional[Skill]:
        return self.db.query(Skill).filter(Skill.name.ilike(name.strip())).first()

    def list_skills(
        self,
        search: Optional[str] = None,
        category: Optional[str] = None,
        page: int = 1,
        page_size: int = 50
    ) -> Tuple[List[Skill], int]:
        query = self.db.query(Skill)

        if search:
            pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Skill.name.ilike(pattern),
                    Skill.category.ilike(pattern),
                    Skill.description.ilike(pattern)
                )
            )

        if category and category.lower() != "all":
            query = query.filter(Skill.category.ilike(category.strip()))

        total = query.count()
        offset = (page - 1) * page_size
        skills = query.order_by(Skill.category.asc(), Skill.name.asc()).offset(offset).limit(page_size).all()

        return skills, total

    def create(self, skill: Skill) -> Skill:
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def update(self, skill: Skill) -> Skill:
        self.db.commit()
        self.db.refresh(skill)
        return skill

    def delete(self, skill: Skill) -> bool:
        self.db.delete(skill)
        self.db.commit()
        return True
