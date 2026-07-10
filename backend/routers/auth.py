from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Form, Request
from models.Users import Users
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.users import UserCreate, UserResponse
from schemas.tokens import Token
from database import get_db
from utils.security import hash_password, verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


def normalize_role(role: str) -> str:
    role_map = {
        "admin": "admin",
        "candidate": "Candidate",
    }
    return role_map.get(str(role).strip().lower(), str(role).strip())


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    try:
        email = user.email.strip().lower()

        result = await db.execute(select(Users).filter(Users.email == email))
        existing_user = result.scalars().first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")

        hashed_password = hash_password(user.password)
        username = (user.name or email).strip()

        result = await db.execute(select(Users).filter(Users.username == username))
        existing_username = result.scalars().first()
        if existing_username:
            username = email

        db_user = Users(
            username=username,
            email=email,
            hashed_password=hashed_password,
            role=normalize_role(user.role),
        )

        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)

        return db_user
    except HTTPException:
        raise
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Email or username already registered")
    except Exception as e:
        await db.rollback()
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while registering the user: {str(e)}")


@router.post("/login", response_model=Token)
async def login(
    request: Request,
    username: Optional[str] = Form(None),
    password: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    try:
        login_email = username
        login_password = password

        if login_email is None or login_password is None:
            try:
                body = await request.json()
            except Exception:
                body = {}

            login_email = login_email or body.get("email") or body.get("username")
            login_password = login_password or body.get("password")

        if not login_email or not login_password:
            raise HTTPException(status_code=400, detail="Email and password are required")

        result = await db.execute(select(Users).filter(Users.email == login_email.strip().lower()))
        existing_user = result.scalars().first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(login_password, existing_user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect password")
        access_token = create_access_token(data={"user_id": existing_user.id, "role": existing_user.role})
        return {"access_token": access_token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"An error occurred while logging in: {str(e)}")
