"""FastAPI 应用入口

纯 Web 版本特点：
- 没有任何前端框架（无 Vue, 无 HTMX, 无 JS 框架）
- 传统服务端渲染，每个操作整页刷新
- 这就是 ASP Classic / PHP 时代最原生的 Web 交互方式
- 对比 app-1 (HTMX) 可以直观感受「局部刷新」带来的体验提升
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
templates = Jinja2Templates(directory="app-2/templates")

# 注册路由
app.include_router(todos.router)


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    """首页 - 显示完整页面（含列表和新增表单）"""
    todos_list = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos_list
    })


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app-2/static"), name="static")
