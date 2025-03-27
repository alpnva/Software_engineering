from pydantic import BaseModel
from typing import List

class Income(BaseModel):
    title: str
    amount: float

class Expense(BaseModel):
    title: str
    amount: float

class Budget(BaseModel):
    incomes: List[Income] = []
    expenses: List[Expense] = []