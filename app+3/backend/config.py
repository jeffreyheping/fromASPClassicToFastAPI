"""应用配置"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(os.path.dirname(BASE_DIR))  # app+3/backend → app+3 → 根目录
DB_PATH = os.path.join(ROOT_DIR, "todo+3.db")

# SQLAlchemy 连接 URI
DB_URI = f"sqlite:///{DB_PATH}"
