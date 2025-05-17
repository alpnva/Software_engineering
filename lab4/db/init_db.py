from sqlalchemy.orm import Session
from db.database import engine, Base, User
from db.test_data import USERS_DATA, INCOMES_DATA, EXPENSES_DATA
from passlib.context import CryptContext
from pymongo import MongoClient
import os
import logging

# Настройка логирования 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

client = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017/"))
db_mongo = client["budgeting"]  

incomes_collection = db_mongo["incomes"]
expenses_collection = db_mongo["expenses"]

def init_db():
    # Создание таблиц в PostgreSQL
    Base.metadata.create_all(bind=engine)
    
    # Инициализация сессии для PostgreSQL
    db = Session(bind=engine)
    
    try:
        if db.query(User).count() == 0:
            # Добавление пользователей
            user_objects = []
            for user_data in USERS_DATA:
                user_obj = User(
                    username=user_data["username"],
                    login=user_data["login"],
                    password=pwd_context.hash(user_data["password"]),
                    role=user_data["role"]
                )
                user_objects.append(user_obj)
            db.add_all(user_objects)
            db.flush()  # Сохраняем, чтобы получить id
            
            # Сопоставляем логины и id
            login_to_user_id = {user.login: user.id for user in user_objects}
            
            # Добавление доходов в MongoDB
            income_objects = [
                {
                    "amount": income["amount"],
                    "description": income["description"],
                    "user_login": income["user_login"]
                }
                for income in INCOMES_DATA
            ]
            incomes_collection.insert_many(income_objects)
            
            # Добавление расходов в MongoDB
            expense_objects = [
                {
                    "amount": expense["amount"],
                    "description": expense["description"],
                    "user_login": expense["user_login"]
                }
                for expense in EXPENSES_DATA
            ]
            expenses_collection.insert_many(expense_objects)
            
            db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при инициализации БД: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_db()