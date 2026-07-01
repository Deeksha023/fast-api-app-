from pydantic import BaseModel
from typing import Optional
from .job import JobResponse

from typing import Optional
from pydantic import BaseModel

class CompanyBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None

class CompanyCreate(CompanyBase):
    name: str
    email: str
    phone: str
    location: str

class CompanyUpdate(CompanyBase):
    pass

class CompanyResponse(CompanyBase):
    pass


class CompanyResponse(CompanyBase):
    id: int
    jobs: list[JobResponse]

    class Config:
        from_attributes = True