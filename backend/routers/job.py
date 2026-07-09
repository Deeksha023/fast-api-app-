from fastapi import APIRouter, HTTPException, Depends, status
from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from models.company import Company
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/job", tags=["job"])
job = []

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def create_job(job_create: JobCreate, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    try:
        payload = job_create.dict(exclude={"company_name"})
        if not payload.get("company_id") and job_create.company_name:
            result = await db.execute(select(Company).filter(Company.name == job_create.company_name))
            company = result.scalar_one_or_none()
            if company is None:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company '{job_create.company_name}' not found")
            payload["company_id"] = company.id

        db_job = Job(**payload)
        db.add(db_job)
        await db.commit()
        await db.refresh(db_job)
        return db_job
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error creating job: {str(e)}")

@router.get("/", status_code=status.HTTP_200_OK, response_model=list[JobResponse])
async def get_all_job(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(select(Job))
        jobs = result.scalars().all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error fetching jobs: {str(e)}")
    return jobs

@router.get("/{job_id}", status_code=status.HTTP_200_OK, response_model=JobResponse)
async def get_job(job_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Job).filter(Job.id == job_id))
    job = result.scalar_one_or_none()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
    return job

@router.put("/{job_id}", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
async def update_job(job_id: int, job_update: JobUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    result = await db.execute(select(Job).filter(Job.id == job_id))
    db_job = result.scalar_one_or_none()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")

    update_data = job_update.dict(exclude={"company_name"}, exclude_unset=True)
    if not update_data.get("company_id") and job_update.company_name:
        company_result = await db.execute(select(Company).filter(Company.name == job_update.company_name))
        company = company_result.scalar_one_or_none()
        if company is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company '{job_update.company_name}' not found")
        update_data["company_id"] = company.id

    for key, value in update_data.items():
        setattr(db_job, key, value)
    await db.commit()
    await db.refresh(db_job)
    return db_job

@router.delete("/{job_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_job(job_id: int, db: AsyncSession = Depends(get_db), current_user = Depends(role_required(["admin"]))):
    db_job = await db.execute(select(Job).filter(Job.id == job_id))
    db_job = db_job.scalar_one_or_none()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
    await db.delete(db_job)
    await db.commit()
    return {"message": "Job deleted successfully"}


# @router.get("/")
# def read_company():
#     return {"company": "Company root."}

# @router.get("/{company_id}")
# def read_company(company_id: int):
#     return {"company_id": company_id}