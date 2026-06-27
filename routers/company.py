from fastapi import APIRouter, HTTPException, Depends, status
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models.company import Company
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/company", tags=["company"])

company = []

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
def create_company(company_create: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(**company_create.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyResponse])
def get_all_company():
    return company

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
def get_company(company_id: int):
    return company[company_id]

# @router.get("/")
# def read_company():
#     return {"company": "Company root."}

# @router.get("/{company_id}")
# def read_company(company_id: int):
#     return {"company_id": company_id}

@router.put("/{company_id}", status_code=status.HTTP_201_CREATED)
def update_company(company_id: int, company_update: CompanyUpdate):
    company[company_id] = company_update
    return company

@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int):
    company.pop(company_id)
    return company