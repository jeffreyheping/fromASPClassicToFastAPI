"""Todo HTMX 路由 - 服务端渲染"""
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Todo

router = APIRouter(prefix="/todos", tags=["todos"])

# 模板引擎（供路由使用）
templates = Jinja2Templates(directory="app-1/templates")


@router.get("/list")
def todo_list(request: Request, db: Session = Depends(get_db)):
    """HTMX: 获取待办列表片段（用于局部刷新）"""
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@router.post("")
def create_todo(
    request: Request,
    info: str = Form(...),
    db: Session = Depends(get_db)
):
    """HTMX: 新增待办"""
    todo = Todo(info=info)
    db.add(todo)
    db.commit()
    db.refresh(todo)

    # 返回更新后的列表
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@router.put("/{todo_id}/toggle")
def toggle_todo(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """HTMX: 切换完成状态"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.status = 1 - (todo.status or 0)
        db.commit()

    # 返回更新后的列表
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@router.get("/{todo_id}/edit")
def edit_form(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """HTMX: 获取编辑表单"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    return templates.TemplateResponse("partials/edit_form.html", {
        "request": request,
        "todo": todo
    })


@router.put("/{todo_id}")
def update_todo(
    request: Request,
    todo_id: int,
    info: str = Form(...),
    db: Session = Depends(get_db)
):
    """HTMX: 更新待办"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.info = info
        db.commit()

    # 返回更新后的列表
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@router.delete("/{todo_id}")
def delete_todo(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """HTMX: 删除待办"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()

    # 返回更新后的列表
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })
