"""FastAPI 应用入口 - 双 UI 架构

外部客人 → /      → Vue.js SPA → /api/todos (JSON)
内部员工 → /internal → HTMX 页面  → /todos    (HTML 片段)

两套 UI 共享同一个 FastAPI 实例 + 同一套 core/services 业务逻辑层。
"""
from pathlib import Path
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .core.database import engine, Base, get_db
from .core import services
from .routers.api import todos as api_todos
from .routers.web import todos as web_todos

# 创建数据库表（必须在 engine 创建之后、首次请求之前）
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App - Dual UI", version="1.0.0")

# 模板引擎（绝对路径，不依赖运行时当前目录）
_tpl_dir = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(_tpl_dir))

# 注册两套路由
app.include_router(api_todos.router)   # /api/todos → JSON
app.include_router(web_todos.router)   # /todos    → HTML 片段


@app.get("/")
def index_vue(request: Request):
    """外部客人入口 - Vue.js SPA"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/internal")
def index_internal(request: Request, db: Session = Depends(get_db)):
    """内部员工入口 - HTMX 页面"""
    todos = services.get_all(db)
    return templates.TemplateResponse("internal.html", {
        "request": request,
        "todos": todos,
    })


# 静态文件挂载（绝对路径）
_static_dir = Path(__file__).resolve().parent / "static"
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")
