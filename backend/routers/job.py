from fastapi import APIRouter, HTTPException, Depends, status
from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from models.company import Company
from sqlalchemy.orm import session
from database import get_db
from utils.oauth2 import get_current_user, role_required

router = APIRouter(prefix="/job", tags=["job"])

job = []

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=JobResponse)
def create_job(job_create: JobCreate, db: session = Depends(get_db), current_user=Depends(role_required(["admin"]))):
    company = db.query(Company).filter(Company.id == job_create.company_id).first()
    if not company:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Company with id {job_create.company_id} not found"
        )

    db_job = Job(**job_create.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/")
def get_all_job(db: session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/{job_id}")
def get_job(job_id: int, db: session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
    return job

@router.put("/{job_id}")
def update_job(job_id: int, job_update: JobUpdate, db: session = Depends(get_db)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
    for key, value in job_update.dict(exclude_unset=True).items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_company(company_id: int,db: session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Company with id {company_id} not found")
    db.delete(db_company)
    db.commit()
# @router.get("/")
# def read_job():
#     return {"job": "Job root."}

# @router.get("/{job_id}")
# def read_job(job_id: int):
#     return {"job_id": job_id}