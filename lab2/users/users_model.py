from pydantic import BaseModel

class User(BaseModel):
    role: str
    username: str
    login: str
    password: str