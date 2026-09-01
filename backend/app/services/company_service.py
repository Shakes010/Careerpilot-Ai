from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.repositories.company_repository import CompanyRepository
from app.schemas.company import CompanyResponse, CompanyUpdateRequest

class CompanyService:
    def __init__(self, db: Session):
        self.db = db
        self.company_repo = CompanyRepository(db)

    def get_company(self, company_id: str) -> CompanyResponse:
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found."
            )
        return CompanyResponse.model_validate(company)

    def update_company(self, company_id: str, req: CompanyUpdateRequest) -> CompanyResponse:
        company = self.company_repo.get_by_id(company_id)
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Company profile not found."
            )

        update_data = req.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if value is not None:
                setattr(company, key, value)

        updated = self.company_repo.update(company)
        return CompanyResponse.model_validate(updated)
