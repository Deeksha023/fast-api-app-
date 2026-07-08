from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from models.Users import Users
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import Login_User, UserCreate, UserResponse
from schemas.tokens import Token
from database import get_db
from utils.security import hash_password, verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        # Check if the user already exists
        result = await db.execute(select(Users).filter(Users.email == user.email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while registering the user")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Determine a display name from available fields
    name = user.name or user.email

    # Create a new user instance
    db_user = Users(
        name=name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )

    # Add the new user to the database
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    try:
        result = await db.execute(select(Users).filter(Users.email == username))
        existing_user = result.scalars().first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(password, existing_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        access_token = create_access_token(data={"user_id": existing_user.id, "role": existing_user.role})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred while logging in")                                                                                                                                               
    