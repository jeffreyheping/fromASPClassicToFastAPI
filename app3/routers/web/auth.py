"""Web认证路由 - Session登录注册（供HTMX前端使用）"""
from pathlib import Path
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from core.database import get_db
from core.models import User
from core import security

router = APIRouter(prefix="/auth", tags=["auth"])

_tpl_dir = Path(__file__).resolve().parent.parent.parent / "templates"
templates = Jinja2Templates(directory=str(_tpl_dir))


@router.get("/login")
def login_page(request: Request):
    """显示登录页面"""
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """处理登录表单"""
    # 查找用户
    user = db.query(User).filter(User.username == username).first()
    if not user or not security.verify_password(password, user.password_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "error": "用户名或密码错误"},
        )

    # 设置Session
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role

    # 根据角色跳转
    if user.role == "staff":
        return RedirectResponse(url="/internal", status_code=302)
    else:
        return RedirectResponse(url="/", status_code=302)


@router.get("/register")
def register_page(request: Request):
    """显示注册页面"""
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register")
def register(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """处理注册表单"""
    # 检查用户名是否已存在
    existing = db.query(User).filter(User.username == username).first()
    if existing:
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "用户名已存在"},
        )

    # 创建新用户
    user = User(
        username=username,
        password_hash=security.hash_password(password),
        role="guest",
    )
    db.add(user)
    db.commit()

    # 自动登录
    request.session["user_id"] = user.id
    request.session["username"] = user.username
    request.session["role"] = user.role

    # 根据角色跳转（与登录逻辑保持一致）
    if user.role == "staff":
        return RedirectResponse(url="/internal", status_code=302)
    else:
        return RedirectResponse(url="/", status_code=302)


@router.post("/logout")
def logout(request: Request):
    """登出"""
    request.session.clear()
    return RedirectResponse(url="/auth/login", status_code=302)
