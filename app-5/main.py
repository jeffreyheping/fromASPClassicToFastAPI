"""FastAPI 应用入口 — 路由分离版

app-5 的核心教学点：
- 从这里开始，SQL 不再散落在模板文件里
- 路由用装饰器显式声明，模板只负责渲染 HTML
- 和 app-2 的结构完全对齐（main.py + routers/ + templates/），
  但数据库访问仍然用 raw sqlite3

对比 app-6：单文件 server.py → 分层结构
对比 app-2：raw SQL → SQLAlchemy ORM（路由代码再往下改）
"""
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import init_db, get_db
from .routers import todos

# 创建数据库表
init_db()

# 创建 FastAPI 实例
app = FastAPI(title="app-5 路由分离版", version="1.0.0")

# 模板引擎
templates = Jinja2Templates(directory="app-5/templates")

# 注册路由
app.include_router(todos.router)


@app.get("/")
def index(request: Request, db=Depends(get_db)):
    """首页 — 显示完整页面（含列表和新增表单）"""
    todos_list = db.execute(
        "SELECT * FROM todo ORDER BY id DESC"
    ).fetchall()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos_list
    })


# 静态文件挂载
app.mount("/static", StaticFiles(directory="app-5/static"), name="static")
