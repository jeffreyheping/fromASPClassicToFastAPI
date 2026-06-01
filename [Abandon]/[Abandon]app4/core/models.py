"""SQLAlchemy 数据模型"""
from .database import Base
from sqlalchemy import Column, Integer, String


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    info = Column(String(200), nullable=False)
    status = Column(Integer, default=0)  # 0=未完成, 1=已完成


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), default="guest")  # guest / staff
