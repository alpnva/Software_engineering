import jwt
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from .users_service import user_db
from typing import Optional
import os

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_JWT", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

# Создание токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Аутентификация пользователя
def authenticate_user(login: str, password: str):
    for user in user_db:
        if user.login == login and user.password == password:
            return user
    return None

@router.post("/token")
async def check_authenticate_user(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid login or password")

    token = create_access_token({"sub": user.login}, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))

    return {
        "message": "Authentication successful",
        "user": {"username": user.username, "role": user.role},
        "access_token": token,
        "token_type": "bearer"
    }
