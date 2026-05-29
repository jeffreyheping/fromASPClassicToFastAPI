The user is asking about how to design a structure where:
1. External users access Vue UI
2. Internal users access HTMX UI
3. Both use the same FastAPI backend
4. Most backend logic can be reused but returns different formats (JSON vs HTML)

This is a design/architecture question that doesn't require me to execute anything - I just need to provide a thoughtful response. Let me think about the best approach:

**Key Design Considerations:**
1. Backend logic should be reusable
2. Different response formats (JSON for Vue, HTML for HTMX)
3. Shared models, schemas, and core business logic
4. Separate frontend (Vue and HTMX)
5. API routes can dispatch to different response handlers

**Possible Approaches:**

1. **Service Layer Pattern**
   - Core business logic in separate service functions
   - Routes just call services and format response
   - Services don't know about response format

2. **Response Strategy Pattern**
   - Pass a "response format" parameter or detect based on headers
   - Return appropriate format based on caller

3. **Decorator Pattern**
   - Create decorators that handle response formatting

4. **Content Negotiation**
   - Use Accept header to determine response format
   - FastAPI supports this via response_class

**Recommended Structure:**
```
project/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app
│   ├── core/
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy models
│   │   ├── schemas.py       # Pydantic schemas
│   │   └── services.py     # Core business logic (reusable!)
│   ├── api/
│   │   ├── __init__.py
│   │   └── todos.py        # API routes
│   ├── ui_vue/              # Vue frontend


│   │   └── ...
│   └── ui_htmx/            # HTMX frontend
│       └── ...
```

The cleanest approach is separating core business logic into services that handle data operations, while keeping routes thin and focused on request handling. This way, both Vue and HTMX interfaces can call the same service functions, with routes deciding whether to return JSON or HTML based on the client's Accept header.
这是一个很好的架构设计问题。让我为你分析几种可行的方案：

---

## 方案分析

### 核心思想

**把「业务逻辑」和「返回格式」分开**：

```
┌─────────────────────────────────────────────────┐
│                    路由层                         │
│  ┌─────────────┐         ┌─────────────┐       │
│  │ Vue 路由    │         │ HTMX 路由   │       │
│  │ /api/todos  │         │ /todos      │       │
│  └──────┬──────┘         └──────┬──────┘       │
│         │                        │              │
│         └────────┬───────────────┘              │
│                  ▼                             │
│         ┌────────────────┐                    │
│         │   服务层        │  ← 核心业务逻辑    │
│         │   (可复用)      │    不关心返回格式   │
│         └────────┬───────┘                    │
└──────────────────┼───────────────────────────┘
```

---

### 推荐方案：服务层模式

```
todo_project/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── core/                # 核心层（可复用）
│   │   ├── __init__.py
│   │   ├── models.py        # SQLAlchemy 模型
│   │   ├── schemas.py       # Pydantic 模型
│   │   └── services.py      # 核心业务逻辑
│   ├── api/                 # API 层（Vue 用）
│   │   ├── __init__.py
│   │   └── todos.py         # 返回 JSON
│   ├── ui/                  # UI 层（HTMX 用）
│   │   ├── __init__.py
│   │   ├── todos.py         # 返回 HTML 片段
│   │   └── templates/
│   │       └── partials/
│   └── static/              # 静态文件
│       ├── vue/             # Vue 前端
│       └── htmx/            # HTMX 前端
```

---

### 关键设计

**1. 服务层 - 纯业务逻辑，不关心返回格式**：

```python
# core/services.py
from sqlalchemy.orm import Session
from ..models import Todo


class TodoService:
    """待办服务 - 纯业务逻辑，可复用"""

    @staticmethod
    def get_all(db: Session):
        return db.query(Todo).order_by(Todo.id.desc()).all()

    @staticmethod
    def create(db: Session, info: str):
        todo = Todo(info=info)
        db.add(todo)
        db.commit()
        db.refresh(todo)
        return todo

    @staticmethod
    def toggle(db: Session, todo_id: int):
        todo = db.query(Todo).filter(Todo.id == todo_id).first()
        if todo:
            todo.status = 1 - (todo.status or 0)
            db.commit()
        return todo
```

**2. API 路由 - 返回 JSON（Vue 用）**：

```python
# api/todos.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ...core.schemas import TodoSchema
from ...core.services import TodoService
from ...database import get_db

router = APIRouter(prefix="/api/todos", tags=["todos"])

@router.get("", response_model=list[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    return TodoService.get_all(db)

@router.post("", response_model=TodoSchema, status_code=201)
def create_todo(todo_in, db: Session = Depends(get_db)):
    return TodoService.create(db, todo_in.info)
```

**3. UI 路由 - 返回 HTML（HTMX 用）**：

```python
# ui/todos.py
from fastapi import APIRouter, Request, Depends, Form
from sqlalchemy.orm import Session
from ...core.services import TodoService
from ...database import get_db

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/list")
def get_todo_list(request: Request, db: Session = Depends(get_db)):
    todos = TodoService.get_all(db)
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })

@router.post("")
def create_todo(request: Request, info: str = Form(...), db: Session = Depends(get_db)):
    TodoService.create(db, info)
    todos = TodoService.get_all(db)
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })
```

**4. 入口文件注册两套路由**：

```python
# main.py
from fastapi import FastAPI
from .api import todos as api_todos
from .ui import todos as ui_todos

app = FastAPI(title="Todo App")

app.include_router(api_todos.router)  # /api/todos -> JSON
app.include_router(ui_todos.router)   # /todos -> HTML
```

---

### 访问路径

| 用户类型 | 访问地址 | 返回格式 |
|---------|---------|---------|
| 外部用户 | http://example.com/vue/ | Vue SPA |
| 外部 API | http://example.com/api/todos | JSON |
| 内部用户 | http://example.com/htmx/ | HTMX 页面 |
| 内部 HTMX | http://example.com/todos | HTML 片段 |

---

需要我为这个设计方案创建具体的代码实现吗？