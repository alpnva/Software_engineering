from fastapi import FastAPI
from users.users_service import router as user_router
from users.auth import router as auth_router
from budgeting.budgeting_service import router as budget_router

app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(budget_router, prefix="/budget", tags=["budget"])

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Budgeting System"}
