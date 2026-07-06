from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session
from utils.token import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(get_db)):
    current_user = verify_access_token(token, db)
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")  
    return current_user
def role_required(required_role):
    if not isinstance(required_role, (list, tuple, set)):
        required_roles = {required_role}
    else:
        required_roles = set(required_role)

    def role_decorator(current_user = Depends(get_current_user)):
        user_role = None
        if isinstance(current_user, dict):
            user_role = current_user.get("role")
        else:
            user_role = getattr(current_user, "role", None)

        if user_role not in required_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to access this resource")
        return current_user

    return role_decorator

                     