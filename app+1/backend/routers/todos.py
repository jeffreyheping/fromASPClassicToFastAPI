"""Todo 路由 - RESTful API，返回 JSON"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import Todo
from schemas import TodoCreate, TodoUpdate, TodoSchema

router = APIRouter(prefix="/api/todos", tags=["todos"])


@router.get("", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    """获取所有待办事项"""
    return db.query(Todo).order_by(Todo.id.desc()).all()


@router.post("", response_model=TodoSchema, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    """新增待办事项"""
    todo = Todo(info=todo_in.info)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


@router.get("/{todo_id}", response_model=TodoSchema)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """获取单个待办事项"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=TodoSchema)
def update_todo(todo_id: int, todo_in: TodoUpdate, db: Session = Depends(get_db)):
    """更新待办事项内容"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if todo_in.info is not None:
        todo.info = todo_in.info
    db.commit()
    db.refresh(todo)
    return todo


@router.put("/{todo_id}/done", response_model=TodoSchema)
def toggle_done(todo_id: int, db: Session = Depends(get_db)):
    """切换完成状态"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    todo.status = 1 - (todo.status or 0)
    db.commit()
    db.refresh(todo)
    return todo


@router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """删除待办事项"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.delete(todo)
    db.commit()
    return {"success": True}
