"""核心业务逻辑层 - 纯函数，不关心返回格式"""
from sqlalchemy.orm import Session

from .models import Todo


def get_all(db: Session, order_desc=True):
    """获取所有待办，默认按 id 倒序"""
    q = db.query(Todo)
    if order_desc:
        q = q.order_by(Todo.id.desc())
    return q.all()


def get_by_id(db: Session, todo_id: int):
    """按 id 获取单条待办，不存在返回 None"""
    return db.query(Todo).filter(Todo.id == todo_id).first()


def create(db: Session, info: str):
    """新增待办，返回新建对象"""
    todo = Todo(info=info)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def update_info(db: Session, todo_id: int, info: str):
    """更新待办内容，返回更新后的对象；不存在返回 None"""
    todo = get_by_id(db, todo_id)
    if todo:
        todo.info = info
        db.commit()
        db.refresh(todo)
    return todo


def toggle_status(db: Session, todo_id: int):
    """切换完成状态，返回更新后的对象；不存在返回 None"""
    todo = get_by_id(db, todo_id)
    if todo:
        todo.status = 1 - (todo.status or 0)
        db.commit()
        db.refresh(todo)
    return todo


def delete(db: Session, todo_id: int):
    """删除待办，返回是否成功"""
    todo = get_by_id(db, todo_id)
    if todo:
        db.delete(todo)
        db.commit()
        return True
    return False
