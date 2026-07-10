import os
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Deeksha%402005@localhost:5432/student_db"
)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgres://",
        "postgresql+asyncpg://",
        1
    )
elif DATABASE_URL.startswith("postgresql://"):
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1
    )

connect_args = {"statement_cache_size": 0}

if "supabase.com" in DATABASE_URL:
    DATABASE_URL = DATABASE_URL.split("?")[0]
    connect_args["ssl"] = "require"

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    connect_args=connect_args
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)

Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()

