from fastapi import APIRouter, Depends, HTTPException, Form, status
from sqlalchemy.orm import Session
from models.Users import Users
from schemas.users import Login_User, UserCreate, UserResponse
from schemas.tokens import Token
from database import get_db
from utils.security import hash_password, verify_password
from utils.token import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if the user already exists
    existing_user = db.query(Users).filter(Users.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Hash the password
    hashed_password = hash_password(user.password)

    # Determine a display name from available fields
    display_name = user.name or user.email

    # Create a new user instance using the actual table columns
    db_user = Users(
        username=display_name,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role.strip().lower()
    )

    # Add the new user to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.post("/login", response_model=Token)
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    existing_user = db.query(Users).filter(Users.email == username).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_password(password, existing_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")
    access_token = create_access_token(data={"user_id": existing_user.id, "role": existing_user.role})
    return {"access_token": access_token, "token_type": "bearer"}
