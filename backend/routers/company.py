from fastapi import APIRouter, HTTPException, Depends, status, Query
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models.company import Company
from sqlalchemy.orm import Session
from database import get_db, SessionLocal
from utils.oauth2 import role_required, get_current_user

router = APIRouter(prefix="/company", tags=["company"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
):
    db_company = Company(**company.dict())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyResponse])
def get_all_company(
    name: str | None = Query(None, description="Filter by company name"),
    email: str | None = Query(None, description="Filter by company email"),
    phone: str | None = Query(None, description="Filter by company phone number"),
    location: str | None = Query(None, description="Filter by company location"),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(Company)
    if name:
        query = query.filter(Company.name.ilike(f"%{name}%"))
    if email:
        query = query.filter(Company.email.ilike(f"%{email}%"))
    if phone:
        query = query.filter(Company.phone.ilike(f"%{phone}%"))
    if location:
        query = query.filter(Company.location.ilike(f"%{location}%"))

    companies = query.all()
    return companies


@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    return company


# @router.get("/")
# def read_company():
#     return {"company": "Company root."}

# @router.get("/{company_id}")
# def read_company(company_id: int):
#     return {"company_id": company_id}


@router.put("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
def update_company(
    company_id: int,
    company_update: CompanyUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
):

    company = db.query(Company).filter(Company.id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    for key, value in company_update.dict().items():
        setattr(company, key, value)

    db.commit()
    db.refresh(company)

    return company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(role_required(["admin"]))
):

    db_company = db.query(Company).filter(Company.id == company_id).first()

    if not db_company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Company not found"
        )

    db.delete(db_company)
    db.commit()

    return