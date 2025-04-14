from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, ForeignKey, create_engine, Column, Integer, Float, Index
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/budgeting")
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()

def create_tables():
    Base.metadata.create_all(bind=engine)

# Пользователь
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    login = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)

    incomes = relationship("Income", back_populates="user", cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_users_username', 'username', postgresql_using='gin', postgresql_ops={"username": "gin_trgm_ops"}),
        Index('ix_users_login', 'login', postgresql_using='gin', postgresql_ops={"login": "gin_trgm_ops"}),
    )

# Доходы
class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="incomes")

# Расходы
class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="expenses")
