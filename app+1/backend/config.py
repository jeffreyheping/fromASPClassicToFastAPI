"""应用配置"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))  # app+1/backend → app+1 → 根目录
DB_PATH = os.path.join(ROOT_DIR, "todo+1.db")

# SQLAlchemy 连接 URI
DB_URI = f"sqlite:///{DB_PATH}"
