from fastapi import HTTPException, Depends, status
from jose import jwt
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database import get_db
from schemas.tokens import Token
import os
from dotenv import load_dotenv
from models.Users import Users


load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=2)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, db: Session = Depends(get_db)):
    try:
        to_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

    current_user = db.query(Users).filter(Users.id == to_decode.get("user_id")).first()
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    return current_user