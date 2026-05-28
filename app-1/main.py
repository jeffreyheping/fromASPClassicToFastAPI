"""FastAPI 应用入口

HTMX 版本特点：
- 不使用 Vue.js，纯服务端渲染 + 局部刷新
- 通过 hx-* 属性实现 AJAX 请求
- 后端返回 HTML 片段，直接替换 DOM
"""
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import Todo
from .routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App", version="1.0.0")

# 模板引擎
templates = Jinja2Templates(directory="app-1/templates")

# 注册路由
app.include_router(todos.router)


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    """首页 - 显示完整页面"""
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos
    })


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app-1/static"), name="static")
