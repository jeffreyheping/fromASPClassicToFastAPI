"""应用配置"""
from pathlib import Path

# 数据库放在项目根目录（和 app/、app-1/ 平级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "todo_api.db"

# SQLite URI：Windows 路径必须转成正斜杠
DB_URI = f"sqlite:///{DB_PATH.as_posix()}"
