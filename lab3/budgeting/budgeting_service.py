from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from users.auth import router as auth_router, get_current_client
from db.database import User, Income as IncomeModel, Expense as ExpenseModel
from db.sessions import get_db
from .budgeting_model import Income, Expense


app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Budgeting API"}

# Доходы

@app.post("/incomes/", response_model=Income)
async def create_income(income: Income, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    income_obj = IncomeModel(title=income.title, amount=income.amount, user_id=current_user.id)
    db.add(income_obj)
    db.commit()
    db.refresh(income_obj)
    return income_obj

@app.get("/incomes/", response_model=List[Income])
async def get_incomes(db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    return db.query(IncomeModel).filter(IncomeModel.user_id == current_user.id).all()

@app.delete("/incomes/{income_id}", response_model=Income)
async def delete_income(income_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    income = db.get(IncomeModel, income_id)
    if not income or income.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Income not found")
    db.delete(income)
    db.commit()
    return income

# Расходы

@app.post("/expenses/", response_model=Expense)
async def create_expense(expense: Expense, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    expense_obj = ExpenseModel(title=expense.title, amount=expense.amount, user_id=current_user.id)
    db.add(expense_obj)
    db.commit()
    db.refresh(expense_obj)
    return expense_obj


@app.get("/expenses/", response_model=List[Expense])
async def get_expenses(db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    return db.query(ExpenseModel).filter(ExpenseModel.user_id == current_user.id).all()


@app.delete("/expenses/{expense_id}", response_model=Expense)
async def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_client)):
    expense = db.get(ExpenseModel, expense_id)
    if not expense or expense.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return expense