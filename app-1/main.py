"""FastAPI + HTMX 应用入口

HTMX 版本特点：
- 不使用 Vue.js，纯服务端渲染 + 局部刷新
- 通过 hx-* 属性实现 AJAX 请求
- 后端返回 HTML 片段，直接替换 DOM
- 让孩子们理解「局部刷新」的底层原理
"""
from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import Todo

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App - HTMX 版", version="1.0.0")

# 模板引擎
templates = Jinja2Templates(directory="app-1/templates")


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    """首页 - 显示完整页面"""
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos
    })


@app.get("/todos/list")
def todo_list(request: Request, db: Session = Depends(get_db)):
    """HTMX: 获取待办列表片段（用于局部刷新）"""
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@app.post("/todos")
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


@app.put("/todos/{todo_id}/toggle")
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


@app.get("/todos/{todo_id}/edit")
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


@app.put("/todos/{todo_id}")
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


@app.delete("/todos/{todo_id}")
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


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app-1/static"), name="static")
