from typing import List, Tuple
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.skill import Skill
from app.repositories.skill_repository import SkillRepository
from app.schemas.skill import SkillCreateRequest, SkillUpdateRequest, SkillResponse

class SkillService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = SkillRepository(db)

    def list_skills(self, search: str = None, category: str = None, page: int = 1, page_size: int = 50) -> Tuple[List[SkillResponse], int]:
        skills, total = self.repo.list_skills(search=search, category=category, page=page, page_size=page_size)
        return [SkillResponse.model_validate(s) for s in skills], total

    def create_skill(self, req: SkillCreateRequest) -> SkillResponse:
        existing = self.repo.get_by_name(req.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Skill '{req.name.strip()}' already exists in the Skill Library."
            )

        skill = Skill(
            name=req.name.strip(),
            category=req.category.strip() if req.category else "General",
            description=req.description.strip() if req.description else None
        )
        created = self.repo.create(skill)
        return SkillResponse.model_validate(created)

    def update_skill(self, skill_id: str, req: SkillUpdateRequest) -> SkillResponse:
        skill = self.repo.get_by_id(skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found.")

        if req.name and req.name.strip().lower() != skill.name.lower():
            existing = self.repo.get_by_name(req.name)
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Skill '{req.name.strip()}' already exists."
                )
            skill.name = req.name.strip()

        if req.category is not None:
            skill.category = req.category.strip()
        if req.description is not None:
            skill.description = req.description.strip()

        updated = self.repo.update(skill)
        return SkillResponse.model_validate(updated)

    def delete_skill(self, skill_id: str) -> bool:
        skill = self.repo.get_by_id(skill_id)
        if not skill:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found.")
        return self.repo.delete(skill)
