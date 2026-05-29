"""Todo 路由 - 纯服务端渲染，整页刷新

与 app-1 (HTMX) 的关键区别：
- HTMX 版：操作后返回 HTML 片段，HTMX 就地替换 DOM
- 纯 Web 版：操作后 Redirect 到首页，浏览器整页刷新

这就是 ASP Classic 时代的标准做法：
用户点击 → 浏览器发请求 → 服务器处理 → 重定向 → 整页重绘
"""
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Todo

router = APIRouter(prefix="/todos", tags=["todos"])

templates = Jinja2Templates(directory="app-2/templates")


@router.post("")
def create_todo(
    request: Request,
    info: str = Form(...),
    db: Session = Depends(get_db)
):
    """新增待办 → 重定向回首页"""
    todo = Todo(info=info)
    db.add(todo)
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/{todo_id}/edit")
def edit_form(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """编辑待办 → 渲染完整编辑页面"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "todo": todo
    })


@router.post("/{todo_id}")
def update_todo(
    request: Request,
    todo_id: int,
    info: str = Form(...),
    db: Session = Depends(get_db)
):
    """更新待办 → 重定向回首页"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.info = info
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/{todo_id}/toggle")
def toggle_done(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """切换完成状态 → 重定向回首页"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.status = 1 - (todo.status or 0)
        db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/{todo_id}/delete")
def delete_todo(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """删除待办 → 重定向回首页"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    return RedirectResponse(url="/", status_code=303)
