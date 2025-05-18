from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class IncomeCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма дохода")
    description: str = Field(..., min_length=1, max_length=255)
    user_login: str = Field(..., description="Логин пользователя, к которому относится доход")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class ExpenseCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Сумма расхода")
    description: str = Field(..., min_length=1, max_length=255)
    user_login: str = Field(..., description="Логин пользователя, к которому относится расход")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# Используется при возврате с идентификатором
class IncomeResponse(IncomeCreate):
    id: str


class ExpenseResponse(ExpenseCreate):
    id: str


# Модель общего бюджета (если используется как агрегат)
class Budget(BaseModel):
    incomes: List[IncomeResponse] = []
    expenses: List[ExpenseResponse] = []
