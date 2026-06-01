"""SQLAlchemy 数据模型"""
from sqlalchemy import Column, Integer, String

from database import Base


class Todo(Base):
    """待办事项模型"""
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    info = Column(String(500), nullable=False)
    status = Column(Integer, default=0)  # 0=未完成, 1=已完成
