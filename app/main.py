"""FastAPI 应用入口"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import engine, Base
from .routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App", version="1.0.0")

# 模板引擎（官方推荐方式）
templates = Jinja2Templates(directory="app/templates")

# 注册路由（必须在 mount 之前）
app.include_router(todos.router)


@app.get("/")
def index(request: Request):
    """前端单页应用入口
    
    使用 Jinja2Templates 渲染模板，request 对象必须传入模板上下文
    """
    return templates.TemplateResponse("index.html", {"request": request})


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app/static"), name="static")
