import asyncio
from database import SessionLocal
from sqlalchemy import select
from models.company import Company
from models.job import Job

async def check():
    session = SessionLocal()
    result = await session.execute(select(Company))
    companies = result.scalars().all()
    print(f'Total Companies: {len(companies)}')
    
    result = await session.execute(select(Job))
    jobs = result.scalars().all()
    print(f'Total Jobs: {len(jobs)}')
    
    if companies:
        for c in companies:
            print(f'  - {c.name}: {len(c.jobs) if c.jobs else 0} jobs')

asyncio.run(check())
