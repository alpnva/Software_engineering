from fastapi import HTTPException, Depends, Query, APIRouter
from .users_model import User
from typing import List

router = APIRouter()

user_db = [User(role="admin", username="Ivan Ivanov", login="admin", password="secret")]

@router.post("/users/", response_model=User)
async def create_user(user: User):
    for users in user_db:
        if users.login == user.login:
            raise HTTPException(status_code=400, detail="User with this login already exists")
    user_db.append(user)
    return user

# Список всех пользователей
@router.get("/users/", response_model=List[User])
async def get_user_all():
    return user_db

# Список пользователей по логину
@router.get('/users/{user_login}', response_model=User)
async def get_user_login(user_login: str):
    for user in user_db:
        if user.login == user_login:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# Список пользователей по имени и фамилии
@router.get('/users', response_model=List[User])
async def get_user_name(user_name: str = Query(...)):
    res = []
    for user in user_db:
        if user_name.lower() in user.username.lower():
            res.append(user)
    if not res:
        raise HTTPException(status_code=404, detail="User not found")
    return res
