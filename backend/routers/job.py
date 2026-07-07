from fastapi import APIRouter, HTTPException, Depends, status
from schemas.job import JobCreate, JobUpdate, JobResponse
from models.job import Job
from models.company import Company
from sqlalchemy import func
from sqlalchemy.orm import Session
from database import get_db
from utils.oauth2 import get_current_user

router = APIRouter(prefix="/job", tags=["job"])


def get_or_create_company_id(db: Session, company_id: int | None = None, company_name: str | None = None):
    clean_name = company_name.strip() if company_name else ""

    if clean_name:
        company = db.query(Company).filter(func.lower(Company.name) == clean_name.lower()).first()
        if company:
            return company.id

        company = Company(name=clean_name)
        db.add(company)
        db.flush()
        return company.id

    if company_id:
        company = db.query(Company).filter(Company.id == company_id).first()
        if not company:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Company with id {company_id} not found"
            )
        return company.id

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Company name is required"
    )


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=JobResponse)
def create_job(job_create: JobCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    job_data = job_create.dict()
    company_name = job_data.pop("company_name", None)
    job_data["company_id"] = get_or_create_company_id(db, job_data.get("company_id"), company_name)

    db_job = Job(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.get("/", response_model=list[JobResponse])
def get_all_job(db: Session = Depends(get_db)):
    jobs = db.query(Job).all()
    return jobs

@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
    return job

@router.put("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job_update: JobUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")

    update_data = job_update.dict(exclude_unset=True)
    company_name = update_data.pop("company_name", None)
    if company_name is not None or "company_id" in update_data:
        update_data["company_id"] = get_or_create_company_id(db, update_data.get("company_id"), company_name)

    for key, value in update_data.items():
        setattr(db_job, key, value)
    db.commit()
    db.refresh(db_job)
    return db_job

@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    db_job = db.query(Job).filter(Job.id == job_id).first()
    if not db_job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with id {job_id} not found")
    db.delete(db_job)
    db.commit()
