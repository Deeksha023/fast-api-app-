from fastapi import APIRouter, HTTPException, Depends, status
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse 
from models.company import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/company", tags=["company"])
company = []

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def create_company(company_create: CompanyCreate, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    try:
        db_company = Company(**company_create.dict())
        db.add(db_company)
        await db.commit()
        await db.refresh(db_company)
        return db_company
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error creating company: {str(e)}")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyResponse])
async def get_all_company(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Company))
        companies = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error fetching companies: {str(e)}")
    return companies

@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    company = result.scalar_one_or_none()
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")
    return company

@router.put("/{company_id}", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def update_company(company_id: int, company_update: CompanyUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    db_company = result.scalar_one_or_none()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")
    for key, value in company_update.dict().items():
        setattr(db_company, key, value) #auto changes value in api by setattr function
    await db.commit()
    await db.refresh(db_company) #it makes a new object with updated values and returns it to the user
    return db_company

@router.delete("/{company_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    db_company = await db.execute(select(Company).filter(Company.id == company_id))
    db_company = db_company.scalar_one_or_none()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")
    await db.delete(db_company)
    await db.commit()
    return {"message": "Company deleted successfully"}


# @router.get("/")
# def read_company():
#     return {"company": "Company root."}

# @router.get("/{company_id}")
# def read_company(company_id: int):
#     return {"company_id": company_id}