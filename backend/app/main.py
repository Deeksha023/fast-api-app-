from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from models import job as job_model, company as company_model, Users as user_model
from routers import company, job,auth,chat


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create database tables
Base.metadata.create_all(bind=engine)

print(engine)

app.include_router(company.router)
app.include_router(job.router)
app.include_router(auth.router)
app.include_router(chat.router)

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/about")
def read_about():
    return {"about": "This is about page"}


@app.get("/contact")
def read_contact():
    return {"contact": "This is contact page"}