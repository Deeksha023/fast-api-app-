from fastapi import APIRouter
from schemas.company import CompanyCreate,CompanyUpdate 

router=APIRouter(prefix="/company", tags=["company"])
company=[]
@router.post("/")
def create_company(company_create:CompanyCreate):
    company.append(company_create)
    return company

@router.get("/")
def get_all_company():
    return company

@router.get("/{company_id}")
def get_company(company_id:int):
    return company[company_id]
# @router.get("/")
# def read_company():
#     return {"company": "Company root."}

# @router.get("/{company_id}")
# def read_company(company_id: int):
#     return {"company_id": company_id}

@router.put("/{company_id}")
def update_company(company_id: int, company_update: CompanyUpdate):
    company[company_id] = company_update
    return company


@router.delete("/{company_id}")
def delete_company(company_id: int):
    company.pop(company_id)
    return company 