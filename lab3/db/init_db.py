from sqlalchemy.orm import Session
from db.database import engine, Base, User, Income, Expense
from db.test_data import USERS_DATA, INCOMES_DATA, EXPENSES_DATA
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def init_db():
    Base.metadata.create_all(bind=engine)
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

            # Добавление доходов
            income_objects = [
                Income(
                    amount=income["amount"],
                    description=income["description"],
                    user_id=login_to_user_id[income["user_login"]]
                )
                for income in INCOMES_DATA
            ]
            db.add_all(income_objects)

            # Добавление расходов
            expense_objects = [
                Expense(
                    amount=expense["amount"],
                    description=expense["description"],
                    user_id=login_to_user_id[expense["user_login"]]
                )
                for expense in EXPENSES_DATA
            ]
            db.add_all(expense_objects)

            db.commit()

    except Exception as e:
        db.rollback()
        print(f"Ошибка при инициализации БД: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()
