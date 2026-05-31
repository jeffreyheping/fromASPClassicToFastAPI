"""数据库连接管理 — raw sqlite3

与 app-6 用完全相同的 SQL，但把连接管理抽到了单独模块。
学生在这里第一次看到「数据库访问层」的雏形。
"""
import sqlite3

from .config import DB_PATH


def init_db():
    """建表（应用启动时调用一次）"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS todo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        info TEXT NOT NULL,
        status INTEGER DEFAULT 0
    )''')
    conn.commit()
    conn.close()


def get_db():
    """FastAPI 依赖注入：获取数据库连接

    和 app-2 的 get_db() 签名一模一样（都是生成器），
    到了 app-2 换成 SQLAlchemy 时，路由代码几乎不用改。
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()
