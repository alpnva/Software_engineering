from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from db.database import User  # SQLAlchemy модель
from db.sessions import get_db
from .users_model import UserCreate, UserResponse, UserUpdate
from .auth import get_current_client  # проверка прав
from .auth import router as auth_router

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Budgeting System - Users"}

# Создание нового пользователя
@app.post("/users/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.login == user.login).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Login already exists")

    user_obj = User(**user.model_dump())
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

# Поиск пользователя по логину
@app.get("/users/by_login/{login}", response_model=UserResponse)
def get_user_by_login(login: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.query(User).filter(User.login == login).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Поиск по маске имени/фамилии
@app.get("/users/search/", response_model=List[UserResponse])
def search_users_by_mask(mask: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    users = db.query(User).filter(User.username.ilike(f"%{mask}%")).all()
    return users

# Обновление данных пользователя
@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, update_data: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in update_data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

# Удаление пользователя
@app.delete("/users/{user_id}", response_model=UserResponse)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
