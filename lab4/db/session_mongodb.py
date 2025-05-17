from pymongo import MongoClient
from db.test_data import INCOMES_DATA, EXPENSES_DATA
import os
import logging

# Настройка логирования 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

client = MongoClient(os.getenv("MONGO_URL", "mongodb://mongo:27017/"))
db = client["budgeting"]  

# Создание коллекций для доходов и расходов
incomes_collection = db["incomes"]
expenses_collection = db["expenses"]

# Создание индексов для быстрого поиска
incomes_collection.create_index("user_login")
expenses_collection.create_index("user_login")

result_incomes = incomes_collection.insert_many(INCOMES_DATA)
result_expenses = expenses_collection.insert_many(EXPENSES_DATA)

logger.info(f"Inserted {len(result_incomes.inserted_ids)} incomes.")
logger.info(f"Inserted {len(result_expenses.inserted_ids)} expenses.")

logger.info("Инициализация базы данных бюджетирования выполнена.")

