from fastapi import FastAPI, HTTPException, APIRouter
from .budgeting_model import Income, Expense, Budget
from typing import List

router = APIRouter()

budget_db = Budget()

# Добавление дохода
@router.post("/income/")
async def create_income(income: Income):
    budget_db.incomes.append(income)
    return {"message": "Income added successfully"}

# Получение списка доходов
@router.get("/income/", response_model=List[Income])
async def list_income():
    return budget_db.incomes

# Добавление расхода
@router.post("/expense/")
async def create_expense(expense: Expense):
    budget_db.expenses.append(expense)
    return {"message": "Expense added successfully"}

# Получение списка расходов
@router.get("/expense/", response_model=List[Expense])
async def list_expense():
    return budget_db.expenses
