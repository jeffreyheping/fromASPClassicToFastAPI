"""FastAPI 应用入口

Vue 版本特点：
- 前后端分离，前端使用 Vue.js 3
- 后端提供 RESTful API，返回 JSON
- 前端通过 fetch 调用 API，自行渲染页面
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import engine, Base
from .routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App", version="1.0.0")

# 模板引擎
templates = Jinja2Templates(directory="app/templates")

# 注册路由
app.include_router(todos.router)


@app.get("/")
def index(request: Request):
    """首页 - 前端单页应用入口"""
    return templates.TemplateResponse("index.html", {"request": request})


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app/static"), name="static")
