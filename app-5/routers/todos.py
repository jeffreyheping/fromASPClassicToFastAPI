"""Todo 路由 — raw sqlite3 + Jinja2

与 app-6 的对比：
- app-6：SQL 写在 Mako 模板里，每个操作一个 .mako 文件
- app-5：SQL 抽到路由函数里，模板只负责渲染 HTML

与 app-2 的对比：
- app-5：conn.execute("INSERT INTO todo ...")    ← raw SQL
- app-2：db.add(Todo(info=info)); db.commit()     ← ORM

路由结构、模板、CSS 完全一致，方便对比学习。
"""
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])

templates = Jinja2Templates(directory="app-5/templates")


@router.post("")
def create_todo(
    request: Request,
    info: str = Form(...),
    db=Depends(get_db)
):
    """新增待办 → 重定向回首页"""
    db.execute("INSERT INTO todo (info, status) VALUES (?, 0)", (info,))
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/{todo_id}/edit")
def edit_form(
    request: Request,
    todo_id: int,
    db=Depends(get_db)
):
    """编辑待办 → 渲染编辑页面"""
    todo = db.execute(
        "SELECT * FROM todo WHERE id = ?", (todo_id,)
    ).fetchone()
    return templates.TemplateResponse("edit.html", {
        "request": request,
        "todo": todo
    })


@router.post("/{todo_id}")
def update_todo(
    request: Request,
    todo_id: int,
    info: str = Form(...),
    db=Depends(get_db)
):
    """更新待办 → 重定向回首页"""
    db.execute(
        "UPDATE todo SET info = ? WHERE id = ?", (info, todo_id)
    )
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/{todo_id}/toggle")
def toggle_done(
    request: Request,
    todo_id: int,
    db=Depends(get_db)
):
    """切换完成状态 → 重定向回首页"""
    db.execute(
        "UPDATE todo SET status = 1 - COALESCE(status, 0) WHERE id = ?",
        (todo_id,)
    )
    db.commit()
    return RedirectResponse(url="/", status_code=303)


@router.get("/{todo_id}/delete")
def delete_todo(
    request: Request,
    todo_id: int,
    db=Depends(get_db)
):
    """删除待办 → 重定向回首页"""
    db.execute("DELETE FROM todo WHERE id = ?", (todo_id,))
    db.commit()
    return RedirectResponse(url="/", status_code=303)
