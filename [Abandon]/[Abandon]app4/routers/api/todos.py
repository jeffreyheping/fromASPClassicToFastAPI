"""Todo 路由 - RESTful API，返回 JSON（供 Vue.js 前端调用）

所有接口需要 OAuth2 JWT 认证（Authorization: Bearer <token>）。
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core import schemas, services
from ...core.security import get_current_user_oauth2

router = APIRouter(prefix="/api/todos", tags=["api"])


@router.get("", response_model=List[schemas.TodoSchema])
def get_todos(
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_oauth2),
):
    """获取所有待办事项"""
    return services.get_all(db)


@router.post("", response_model=schemas.TodoSchema, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_in: schemas.TodoCreate,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_oauth2),
):
    """新增待办事项"""
    return services.create(db, todo_in.info)


@router.get("/{todo_id}", response_model=schemas.TodoSchema)
def get_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_oauth2),
):
    """获取单个待办事项"""
    todo = services.get_by_id(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=schemas.TodoSchema)
def update_todo(
    todo_id: int,
    todo_in: schemas.TodoUpdate,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_oauth2),
):
    """更新待办事项内容"""
    if todo_in.info is None:
        raise HTTPException(status_code=400, detail="info is required")
    todo = services.update_info(db, todo_id, todo_in.info)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}/toggle", response_model=schemas.TodoSchema)
def toggle_done(
    todo_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_oauth2),
):
    """切换完成状态"""
    todo = services.toggle_status(db, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.delete("/{todo_id}")
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    _user: dict = Depends(get_current_user_oauth2),
):
    """删除待办事项"""
    if not services.delete(db, todo_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    return {"success": True}
