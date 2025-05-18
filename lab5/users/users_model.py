from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    login: str
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    role: str
    username: str
    login: str

class UserUpdate(BaseModel):
    username: str
    login: str
    password: str
    
    class Config:
        from_attributes = True