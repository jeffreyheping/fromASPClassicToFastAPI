"""Todo 路由 - 服务端渲染，返回 HTML 片段（供 HTMX 前端调用）

所有接口需要 Session 认证（已登录）。
"""
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from core.database import get_db
from core import services
from core.security import get_current_user_session

router = APIRouter(prefix="/todos", tags=["web"])

templates = Jinja2Templates(directory="templates")


@router.get("/list")
def get_todo_list(
    request: Request,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_session),
):
    """获取待办列表片段"""
    todos = services.get_all(db)
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos,
    })


@router.post("")
def create_todo(
    request: Request,
    info: str = Form(...),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_session),
):
    """新增待办事项"""
    services.create(db, info)
    return _render_list(request, db)


@router.get("/{todo_id}/edit")
def get_edit_form(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_session),
):
    """获取编辑表单"""
    todo = services.get_by_id(db, todo_id)
    return templates.TemplateResponse("partials/edit_form.html", {
        "request": request,
        "todo": todo,
    })


@router.put("/{todo_id}")
def update_todo(
    request: Request,
    todo_id: int,
    info: str = Form(...),
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_session),
):
    """更新待办事项内容"""
    services.update_info(db, todo_id, info)
    return _render_list(request, db)


@router.put("/{todo_id}/toggle")
def toggle_done(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_session),
):
    """切换完成状态"""
    services.toggle_status(db, todo_id)
    return _render_list(request, db)


@router.delete("/{todo_id}")
def delete_todo(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_session),
):
    """删除待办事项"""
    services.delete(db, todo_id)
    return _render_list(request, db)


def _render_list(request: Request, db: Session):
    """内部辅助：渲染更新后的列表片段"""
    todos = services.get_all(db)
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos,
    })
