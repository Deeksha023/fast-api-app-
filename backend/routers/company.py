from fastapi import APIRouter, HTTPException, Depends, status
from schemas.company import CompanyCreate, CompanyUpdate, CompanyResponse
from models.company import Company
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from database import get_db
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/company", tags=["company"])
company = []


async def get_company_with_jobs(db: AsyncSession, company_id: int):
    result = await db.execute(
        select(Company)
        .options(selectinload(Company.jobs))
        .filter(Company.id == company_id)
    )
    return result.scalar_one_or_none()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def create_company(company_create: CompanyCreate, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    try:
        company_data = company_create.model_dump()
        db_company = Company(**company_data)
        db.add(db_company)
        await db.flush()
        company_id = db_company.id
        await db.commit()
        return {**company_data, "id": company_id, "jobs": []}
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company email or phone already exists")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error creating company: {str(e)}")


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CompanyResponse])
async def get_all_company(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Company).options(selectinload(Company.jobs)))
        companies = result.scalars().all()
        return companies
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error fetching companies: {str(e)}")


@router.get("/{company_id}", status_code=status.HTTP_200_OK, response_model=CompanyResponse)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    company = await get_company_with_jobs(db, company_id)
    if not company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")
    return company


@router.put("/{company_id}", status_code=status.HTTP_201_CREATED, response_model=CompanyResponse)
async def update_company(company_id: int, company_update: CompanyUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    result = await db.execute(select(Company).filter(Company.id == company_id))
    db_company = result.scalar_one_or_none()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")

    try:
        for key, value in company_update.model_dump(exclude_unset=True).items():
            setattr(db_company, key, value)
        await db.commit()
        updated_company = await get_company_with_jobs(db, company_id)
        return updated_company
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Company email or phone already exists")
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error updating company: {str(e)}")


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_company(company_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    db_company = await db.execute(select(Company).filter(Company.id == company_id))
    db_company = db_company.scalar_one_or_none()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")
    await db.delete(db_company)
    await db.commit()
    return {"message": "Company deleted successfully"}


