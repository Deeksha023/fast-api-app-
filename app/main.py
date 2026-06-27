from fastapi import FastAPI

from database import Base, engine

# Import models before create_all()
from models.company import Company
from models.job import Job

from routers import company, job

app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

print(engine)

app.include_router(company.router)
app.include_router(job.router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/about")
def read_about():
    return {"about": "This is about page"}


@app.get("/contact")
def read_contact():
    return {"contact": "This is contact page"}