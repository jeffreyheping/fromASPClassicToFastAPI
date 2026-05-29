"""应用配置"""
import os
from pathlib import Path

# 数据库放在项目根目录（和 app/、app-1/ 平级）
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DB_PATH = PROJECT_ROOT / "todo4.db"

# 支持环境变量覆盖（测试用 APP4_DATABASE_URL=sqlite:///:memory:）
DATABASE_URL = os.getenv("APP4_DATABASE_URL", f"sqlite:///{DB_PATH.as_posix()}")

# JWT 密钥（生产环境请用环境变量覆盖）
SECRET_KEY = os.getenv("APP4_SECRET_KEY", "dev-secret-change-in-production")
