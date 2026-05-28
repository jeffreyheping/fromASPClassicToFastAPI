# Todo FastAPI one_1 搭建指南

> 照做一定成功版 · 2026 年 5 月

---

## 一、准备工作

### 1.1 确认环境

确保已安装：

- Python 3.10 或更高版本
- pip（Python 包管理器）

验证：

```bash
python3 --version
pip3 --version
```

### 1.2 创建工作目录

```bash
mkdir todo_fastapi_one_1
cd todo_fastapi_one_1
```

> 你可以把 `todo_fastapi_one_1` 换成任何你喜欢的目录名，但后面的命令都要在这个目录下执行。

---

## 二、创建项目目录

```bash
mkdir -p app/routers
mkdir -p app/static/css
mkdir -p app/static/js
mkdir -p app/templates
```

创建完成后，目录结构应该是：

```
todo_fastapi_one_1/
├── app/
│   ├── routers/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── templates/
```

---

## 三、安装依赖

> ⚠️ **重要：版本已锁定！** 本项目的 `requirements.txt` 已锁定所有依赖版本，确保长期稳定运行。请勿随意升级！

创建 `requirements.txt`：

```bash
cat > requirements.txt << 'EOF'
# 版本锁定 - 确保教学项目长期稳定运行
# 更新日期: 2026-05-27
# 测试环境: Python 3.10, Ubuntu 22.04

fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.36
pydantic==2.9.2
jinja2==3.1.2
starlette==0.38.6

# 注意: 不要随意升级版本!
# 如需升级, 请先在测试环境验证所有功能正常
EOF
```

安装所有依赖：

```bash
pip install -r requirements.txt --break-system-packages
```

> 等待安装完成，你会看到 `Successfully installed ...` 的提示。

---

## 四、编写代码（按顺序）

> 下面的代码必须按顺序逐个文件创建。每个文件都要完整复制粘贴，不要漏行。

### 4.1 配置文件

创建 `app/config.py`：

```python
"""应用配置"""
DB_URI = "sqlite:///./todo.db"
```

### 4.2 数据库模块

创建 `app/database.py`：

```python
"""数据库连接与会话管理"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase as _DeclarativeBase

from .config import DB_URI

engine = create_engine(DB_URI, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(_DeclarativeBase):
    pass


def get_db():
    """FastAPI 依赖注入：获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

> ⚠️ **重要**：SQLAlchemy 2.0 的 Base 定义方式变了！必须用 `class Base(_DeclarativeBase): pass`，不能写成 `Base = DeclarativeBase()`，否则会报错 `TypeError: DeclarativeBase() takes no arguments`。

### 4.3 数据模型

创建 `app/models.py`：

```python
"""SQLAlchemy 数据模型"""
from .database import Base
from sqlalchemy import Column, Integer, String


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True, index=True)
    info = Column(String(200), nullable=False)
    status = Column(Integer, default=0)  # 0=未完成, 1=已完成
```

### 4.4 Pydantic 模型

创建 `app/schemas.py`：

```python
"""Pydantic 数据模型（请求/响应验证）"""
from pydantic import BaseModel
from typing import Optional


class TodoCreate(BaseModel):
    info: str


class TodoUpdate(BaseModel):
    info: Optional[str] = None


class TodoSchema(BaseModel):
    id: int
    info: str
    status: int

    model_config = {"from_attributes": True}
```

> ⚠️ **重要**：Pydantic 2.x 的配置方式变了！必须用 `model_config = {"from_attributes": True}`，不能用旧的 `class Config: orm_mode = True`。

### 4.5 路由模块

创建 `app/routers/__init__.py`（空文件）：

```bash
touch app/routers/__init__.py
```

创建 `app/routers/todos.py`：

```python
"""Todo 路由 - RESTful API，返回 JSON"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Todo
from ..schemas import TodoCreate, TodoUpdate, TodoSchema

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
```

### 4.6 主入口

创建 `app/__init__.py`（空文件）：

```bash
touch app/__init__.py
```

创建 `app/main.py`：

```python
"""FastAPI 应用入口

Vue 版本特点：
- 前后端分离，前端使用 Vue.js 3
- 后端提供 RESTful API，返回 JSON
- 前端通过 fetch 调用 API，自行渲染页面
"""
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .database import engine, Base
from .routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App", version="1.0.0")

# 模板引擎
templates = Jinja2Templates(directory="app/templates")

# 注册路由
app.include_router(todos.router)


@app.get("/")
def index(request: Request):
    """首页 - 前端单页应用入口"""
    return templates.TemplateResponse("index.html", {"request": request})


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app/static"), name="static")
```

> ⚠️ **重要**：`app.mount` 必须在所有路由之后！如果放在前面，会拦截所有请求，导致路由失效。

### 4.7 前端 HTML

创建 `app/templates/index.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App - FastAPI + Vue.js</title>
    <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
</head>
<body>
    <div id="app">
        <!-- 列表视图 -->
        <div v-if="view === 'list'" class="container">
            <h1>📋 待办事项</h1>

            <div class="toolbar">
                <button class="btn btn-primary" @click="view = 'add'">+ 新增</button>
            </div>

            <div v-if="todos.length === 0" class="empty">
                暂无待办事项，点击「+ 新增」添加
            </div>

            <ul class="todo-list">
                <li v-for="todo in todos" :key="todo.id"
                    :class="{ done: todo.status === 1 }">
                    <span class="info" @click="toggleDone(todo.id)">
                        {{ '{{' }} todo.info {{ '}}' }}
                    </span>
                    <span class="actions">
                        <button class="btn btn-sm" @click="editTodo(todo)">✏️</button>
                        <button class="btn btn-sm btn-danger" @click="deleteTodo(todo.id)">🗑️</button>
                    </span>
                </li>
            </ul>
        </div>

        <!-- 新增视图 -->
        <div v-if="view === 'add'" class="container">
            <h1>➕ 新增待办</h1>
            <div class="form-group">
                <textarea v-model="form.info" placeholder="请输入待办内容..." rows="3"></textarea>
            </div>
            <div class="form-actions">
                <button class="btn" @click="view = 'list'">取消</button>
                <button class="btn btn-primary" @click="saveAdd">保存</button>
            </div>
        </div>

        <!-- 编辑视图 -->
        <div v-if="view === 'edit'" class="container">
            <h1>✏️ 编辑待办</h1>
            <div class="form-group">
                <textarea v-model="form.info" placeholder="请输入待办内容..." rows="3"></textarea>
            </div>
            <div class="form-actions">
                <button class="btn" @click="view = 'list'">取消</button>
                <button class="btn btn-primary" @click="saveEdit">更新</button>
            </div>
        </div>
    </div>

    <script src="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <script src="{{ url_for('static', path='/js/app.js') }}"></script>
</body>
</html>
```

> 💡 **重要说明**：
> 
> 1. **静态文件 URL**：使用 `{{ url_for('static', path='...') }}` 生成，这是 Jinja2Templates 的优势——即使静态文件路径变化，模板也能正确生成 URL。
> 
> 2. **Jinja2 与 Vue.js 冲突处理**：两者都使用 `{{ }}` 语法。模板中 `{{ url_for(...) }}` 是 Jinja2 语法，会在服务端渲染时执行；而 `{{ '{{' }} todo.info {{ '}}' }}` 这种写法会让 Jinja2 输出 `{{ todo.info }}`，留给 Vue.js 在浏览器端处理。

### 4.8 前端 CSS

创建 `app/static/css/style.css`：

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    background: #f0f2f5;
    color: #333;
    line-height: 1.6;
}

.container {
    max-width: 600px;
    margin: 40px auto;
    padding: 24px;
    background: #fff;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

h1 {
    font-size: 24px;
    margin-bottom: 20px;
    color: #1a1a2e;
}

.toolbar {
    margin-bottom: 16px;
}

.form-group {
    margin-bottom: 16px;
}

.form-group textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 15px;
    font-family: inherit;
    resize: vertical;
    transition: border-color 0.2s;
}

.form-group textarea:focus {
    outline: none;
    border-color: #4361ee;
}

.form-actions {
    display: flex;
    gap: 8px;
    justify-content: flex-end;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    background: #e0e0e0;
    color: #333;
    transition: background 0.2s;
}

.btn:hover {
    background: #d0d0d0;
}

.btn-primary {
    background: #4361ee;
    color: #fff;
}

.btn-primary:hover {
    background: #3a56d4;
}

.btn-danger {
    background: transparent;
    color: #e63946;
}

.btn-danger:hover {
    background: #fff0f0;
}

.btn-sm {
    padding: 4px 8px;
    font-size: 13px;
}

.todo-list {
    list-style: none;
}

.todo-list li {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 0;
    border-bottom: 1px solid #f0f0f0;
}

.todo-list li:last-child {
    border-bottom: none;
}

.todo-list .info {
    flex: 1;
    cursor: pointer;
    font-size: 15px;
    transition: color 0.2s;
}

.todo-list .info:hover {
    color: #4361ee;
}

.todo-list .done .info {
    text-decoration: line-through;
    color: #999;
}

.todo-list .actions {
    display: flex;
    gap: 4px;
}

.empty {
    text-align: center;
    color: #999;
    padding: 40px 0;
    font-size: 15px;
}
```

### 4.9 前端 JavaScript

创建 `app/static/js/app.js`：

```javascript
const API = '/api/todos';

const { createApp } = Vue;

createApp({
    data() {
        return {
            view: 'list',   // list | add | edit
            todos: [],
            form: { info: '' },
            editingId: null
        };
    },
    mounted() {
        this.loadTodos();
    },
    methods: {
        async loadTodos() {
            const res = await fetch(API);
            this.todos = await res.json();
        },

        async toggleDone(id) {
            await fetch(`${API}/${id}/done`, { method: 'PUT' });
            this.loadTodos();
        },

        editTodo(todo) {
            this.editingId = todo.id;
            this.form.info = todo.info;
            this.view = 'edit';
        },

        async saveAdd() {
            const info = this.form.info.trim();
            if (!info) return;
            await fetch(API, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ info })
            });
            this.form.info = '';
            this.view = 'list';
            this.loadTodos();
        },

        async saveEdit() {
            const info = this.form.info.trim();
            if (!info) return;
            await fetch(`${API}/${this.editingId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ info })
            });
            this.form.info = '';
            this.editingId = null;
            this.view = 'list';
            this.loadTodos();
        },

        async deleteTodo(id) {
            if (!confirm('确定要删除吗？')) return;
            await fetch(`${API}/${id}`, { method: 'DELETE' });
            this.loadTodos();
        }
    }
}).mount('#app');
```

---

## 五、运行项目

确保你在 `todo_fastapi_one_1` 目录下，然后执行：

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

看到以下输出表示启动成功：

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxx] using WatchFiles
INFO:     Started server process [xxxx]
INFO:     Application startup complete.
```

打开浏览器访问：

```
http://localhost:8000
```

---

## 六、验证功能

打开浏览器后，你应该能看到：

1. 📋 待办事项 标题
2. + 新增 按钮
3. 暂无待办事项，点击「+ 新增」添加 提示

**测试步骤：**

| 步骤 | 操作 | 预期结果 |
|------|------|---------|
| 1 | 点击「+ 新增」 | 切换到新增页面 |
| 2 | 输入内容，点击「保存」 | 返回列表，显示新待办 |
| 3 | 点击待办文字 | 文字出现删除线（已完成） |
| 4 | 再次点击待办文字 | 删除线消失（未完成） |
| 5 | 点击 ✏️ | 切换到编辑页面，内容已填入 |
| 6 | 修改内容，点击「更新」 | 返回列表，内容已更新 |
| 7 | 点击 🗑️ | 弹出确认框，确认后待办被删除 |

**API 文档**（FastAPI 自动生成）：

```
http://localhost:8000/docs
```

---

## 七、常见问题

### Q1: `TypeError: DeclarativeBase() takes no arguments`

**原因**：SQLAlchemy 2.0 的写法变了。

**解决**：确保 `database.py` 中使用：

```python
from sqlalchemy.orm import DeclarativeBase as _DeclarativeBase

class Base(_DeclarativeBase):
    pass
```

而不是：

```python
# ❌ 错误写法
Base = DeclarativeBase()
```

### Q2: `ModuleNotFoundError: No module named 'xxx'`

**原因**：依赖没有正确安装，或版本不匹配。

**解决**：严格按照 `requirements.txt` 中的版本安装：

```bash
pip install -r requirements.txt --break-system-packages
```

### Q3: 访问页面 404 Not Found

**原因**：`app.mount` 放在了路由之前，拦截了所有请求。

**解决**：确保 `main.py` 中 `app.mount` 在所有路由注册**之后**：

```python
# ✅ 正确顺序
app.include_router(todos.router)   # 先注册路由
app.mount("/static", ...)          # 再挂载静态文件
```

### Q4: 数据库表没有自动创建

**原因**：`Base.metadata.create_all(bind=engine)` 没有执行。

**解决**：确认 `main.py` 中有这行代码。如果表结构变了，手动删除 `todo.db` 文件，下次启动会重新创建。

### Q5: 端口 8000 被占用

**解决**：换一个端口：

```bash
uvicorn app.main:app --port 8080 --reload
```

---

## 附录

### 版本信息

| 组件 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.115.0 | Web 框架 |
| Uvicorn | 0.32.0 | ASGI 服务器 |
| SQLAlchemy | 2.0.36 | ORM |
| Pydantic | 2.9.2 | 数据验证 |
| Jinja2 | 3.1.2 | 模板引擎 |
| Starlette | 0.38.6 | ASGI 工具集 |

### 文件清单

```
todo_fastapi_one_1/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── todos.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       └── index.html
├── requirements.txt
└── README.md
```

共 **10 个代码文件**，全部创建完成后即可运行。

---

> **关于版本锁定**
> 
> 本项目的 `requirements.txt` 已锁定所有依赖版本。这是教学项目的最佳实践，确保：
> 
> 1. **可复现性**：无论何时安装，都能得到相同的运行环境
> 2. **稳定性**：不会因为依赖升级引入 breaking changes
> 3. **教学可靠性**：孩子们按照步骤操作，一定能成功
> 
> 如需升级版本，请先在测试环境验证所有功能正常，然后更新 `requirements.txt` 和本文档。
