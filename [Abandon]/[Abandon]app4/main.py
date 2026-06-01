"""FastAPI 应用入口 - 双 UI 架构（app4版本）

外部客人 → /      → Vue.js SPA → /api/todos (JSON)
内部员工 → /internal → HTMX 页面  → /todos    (HTML 片段)

两套 UI 共享同一个 FastAPI 实例 + 同一套 core/services 业务逻辑层。
"""
from pathlib import Path
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from .core.database import engine, Base, get_db
from .core.config import SECRET_KEY as SESSION_SECRET
from .core import services
from .core.security import get_current_user_session
from .routers.api import todos as api_todos
from .routers.web import todos as web_todos
from .routers.api import auth as api_auth
from .routers.web import auth as web_auth


def create_app() -> FastAPI:
    """创建 FastAPI 应用实例（工厂函数，测试可独立调用）"""
    app = FastAPI(title="Todo App - Dual UI (app4)", version="1.0.0")

    # 添加 Session 中间件（用于 HTMX 登录）
    app.add_middleware(
        SessionMiddleware,
        secret_key=SESSION_SECRET,
        max_age=3600,  # Session 有效期 1 小时
    )

    # 模板引擎（绝对路径，不依赖运行时当前目录）
    _tpl_dir = Path(__file__).resolve().parent / "templates"
    templates = Jinja2Templates(directory=str(_tpl_dir))

    # 401 异常处理：浏览器请求 → 重定向到登录页，API 请求 → 返回 JSON
    @app.exception_handler(HTTPException)
    async def auth_exception_handler(request: Request, exc: HTTPException):
        if exc.status_code == 401:
            accept = request.headers.get("accept", "")
            if "text/html" in accept:
                return RedirectResponse(url="/auth/login", status_code=302)
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

    # 注册路由
    app.include_router(api_todos.router)   # /api/todos → JSON
    app.include_router(web_todos.router)   # /todos    → HTML 片段
    app.include_router(api_auth.router)    # /api/auth → JWT 认证
    app.include_router(web_auth.router)    # /auth     → Session 认证


    @app.get("/")
    def index_vue(request: Request):
        """外部客人入口 - Vue.js SPA"""
        return templates.TemplateResponse("index.html", {"request": request})


    @app.get("/internal")
    def index_internal(
        request: Request,
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user_session),
    ):
        """内部员工入口 - HTMX 页面（需要Session登录）"""
        todos = services.get_all(db)
        return templates.TemplateResponse("internal.html", {
            "request": request,
            "todos": todos,
            "username": user["username"],
            "role": user["role"],
        })


    # 静态文件挂载（绝对路径）
    _static_dir = Path(__file__).resolve().parent / "static"
    app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")

    return app


# 生产环境：建表 + 创建 app
Base.metadata.create_all(bind=engine)
app = create_app()
