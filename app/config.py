"""应用配置"""
import os

APP_NAME = os.path.basename(os.path.dirname(__file__))
DB_URI = "sqlite:///./todo.db"
