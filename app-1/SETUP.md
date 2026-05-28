# Todo FastAPI + HTMX 搭建指南

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

---

## 二、创建项目目录

```bash
mkdir -p app-1/routers
mkdir -p app-1/static/css
mkdir -p app-1/templates/partials
```

创建完成后，目录结构应该是：

```
app-1/
├── routers/
├── static/
│   └── css/
└── templates/
    └── partials/
```

---

## 三、安装依赖

使用项目根目录的 `requirements.txt`（版本已锁定）：

```bash
pip install -r ../requirements.txt --break-system-packages
```

---

## 四、编写代码（按顺序）

### 4.1 配置文件

创建 `app-1/config.py`：

```python
"""应用配置"""
DB_URI = "sqlite:///./todo_htmx.db"
```

### 4.2 数据库模块

创建 `app-1/database.py`：

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

### 4.3 数据模型

创建 `app-1/models.py`：

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

### 4.4 路由模块

创建 `app-1/routers/__init__.py`（空文件）：

```bash
touch app-1/routers/__init__.py
```

创建 `app-1/routers/todos.py`：

```python
"""Todo 路由 - 服务端渲染，返回 HTML 片段"""
from fastapi import APIRouter, Request, Depends, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Todo

router = APIRouter(prefix="/todos", tags=["todos"])

# 模板引擎
templates = Jinja2Templates(directory="app-1/templates")


@router.get("/list")
def get_todo_list(request: Request, db: Session = Depends(get_db)):
    """获取待办列表片段"""
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
    """新增待办事项"""
    todo = Todo(info=info)
    db.add(todo)
    db.commit()
    db.refresh(todo)

    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@router.get("/{todo_id}/edit")
def get_edit_form(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """获取编辑表单"""
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
    """更新待办事项内容"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.info = info
        db.commit()

    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })


@router.put("/{todo_id}/toggle")
def toggle_done(
    request: Request,
    todo_id: int,
    db: Session = Depends(get_db)
):
    """切换完成状态"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.status = 1 - (todo.status or 0)
        db.commit()

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
    """删除待办事项"""
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()

    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })
```

### 4.5 主入口

创建 `app-1/__init__.py`（空文件）：

```bash
touch app-1/__init__.py
```

创建 `app-1/main.py`：

```python
"""FastAPI 应用入口

HTMX 版本特点：
- 不使用 Vue.js，纯服务端渲染 + 局部刷新
- 通过 hx-* 属性实现 AJAX 请求
- 后端返回 HTML 片段，直接替换 DOM
"""
from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from .database import engine, Base, get_db
from .models import Todo
from .routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo App", version="1.0.0")

# 模板引擎
templates = Jinja2Templates(directory="app-1/templates")

# 注册路由
app.include_router(todos.router)


@app.get("/")
def index(request: Request, db: Session = Depends(get_db)):
    """首页 - 显示完整页面"""
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "todos": todos
    })


# 静态文件挂载（必须在所有路由之后）
app.mount("/static", StaticFiles(directory="app-1/static"), name="static")
```

### 4.6 前端 CSS

创建 `app-1/static/css/style.css`：

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

.add-form {
    display: flex;
    gap: 8px;
    margin-bottom: 20px;
}

.add-form input {
    flex: 1;
    padding: 12px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    font-size: 15px;
    font-family: inherit;
}

.add-form input:focus {
    outline: none;
    border-color: #4361ee;
}

.edit-form {
    display: flex;
    gap: 8px;
    flex: 1;
}

.edit-form input {
    flex: 1;
    padding: 8px 12px;
    border: 2px solid #4361ee;
    border-radius: 6px;
    font-size: 15px;
    font-family: inherit;
}

.edit-form input:focus {
    outline: none;
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

.htmx-indicator {
    opacity: 0;
    transition: opacity 200ms;
}

.htmx-request .htmx-indicator {
    opacity: 1;
}

.htmx-request.htmx-indicator {
    opacity: 1;
}

.info-box {
    max-width: 600px;
    margin: 20px auto;
    padding: 16px;
    background: #e8f4f8;
    border-radius: 8px;
    font-size: 14px;
    color: #555;
}

.info-box strong {
    color: #333;
}

.info-box code {
    background: #f0f0f0;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
}
```

### 4.7 主页面 HTML

创建 `app-1/templates/index.html`：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Todo App - HTMX 版</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <link rel="stylesheet" href="{{ url_for('static', path='/css/style.css') }}">
</head>
<body>
    <div class="container">
        <h1>📋 待办事项 (HTMX 版)</h1>

        <!-- 新增表单 -->
        <form class="add-form"
              hx-post="/todos"
              hx-target="#todo-list"
              hx-swap="innerHTML"
              hx-on::after-request="this.reset()">
            <input type="text" name="info" placeholder="输入待办事项..." required>
            <button type="submit" class="btn btn-primary">+ 新增</button>
        </form>

        <!-- 待办列表 -->
        <div id="todo-list">
            {% include "partials/todo_list.html" %}
        </div>
    </div>

    <!-- 说明 -->
    <div class="info-box">
        <strong>💡 HTMX 原理说明：</strong><br>
        这个版本没有使用 Vue.js，而是通过 HTMX 的 <code>hx-*</code> 属性实现局部刷新。<br>
        点击「完成」「编辑」「删除」时，浏览器发送 AJAX 请求，后端返回 HTML 片段，HTMX 自动替换页面内容。
    </div>
</body>
</html>
```

### 4.8 待办列表片段

创建 `app-1/templates/partials/todo_list.html`：

```html
<ul class="todo-list">
    {% if todos %}
        {% for todo in todos %}
        <li class="{% if todo.status == 1 %}done{% endif %}">
            <span class="info"
                  hx-put="/todos/{{ todo.id }}/toggle"
                  hx-target="#todo-list"
                  hx-swap="innerHTML">
                {{ todo.info }}
            </span>
            <span class="actions">
                <button class="btn btn-sm"
                        hx-get="/todos/{{ todo.id }}/edit"
                        hx-target="closest li"
                        hx-swap="outerHTML">
                    ✏️
                </button>
                <button class="btn btn-sm btn-danger"
                        hx-delete="/todos/{{ todo.id }}"
                        hx-target="#todo-list"
                        hx-swap="innerHTML"
                        hx-confirm="确定要删除吗？">
                    🗑️
                </button>
            </span>
        </li>
        {% endfor %}
    {% else %}
        <li class="empty">暂无待办事项，在上方输入框添加</li>
    {% endif %}
</ul>
```

### 4.9 编辑表单片段

创建 `app-1/templates/partials/edit_form.html`：

```html
<li>
    <form class="edit-form"
          hx-put="/todos/{{ todo.id }}"
          hx-target="#todo-list"
          hx-swap="innerHTML">
        <input type="text" name="info" value="{{ todo.info }}" required autofocus>
        <button type="submit" class="btn btn-primary btn-sm">保存</button>
        <button type="button" class="btn btn-sm"
                hx-get="/todos/list"
                hx-target="#todo-list"
                hx-swap="innerHTML">
            取消
        </button>
    </form>
</li>
```

---

## 五、运行项目

```bash
uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload
```

看到以下输出表示启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

打开浏览器访问：http://localhost:8003

---

## 六、验证功能

### 测试步骤

| 步骤 | 操作 | 预期结果 |
|------|------|---------|
| 1 | 在输入框输入内容，点击「+ 新增」 | 待办出现在列表中，输入框清空 |
| 2 | 点击待办文字 | 文字出现删除线（已完成） |
| 3 | 再次点击待办文字 | 删除线消失（未完成） |
| 4 | 点击 ✏️ | 该行变成编辑表单 |
| 5 | 修改内容，点击「保存」 | 列表更新，显示新内容 |
| 6 | 点击 🗑️ | 弹出确认框，确认后待办被删除 |

### HTMX 效果观察

打开浏览器开发者工具（F12）→ Network 标签：

1. 点击「+ 新增」时，会看到 POST 请求发送到 `/todos`
2. 后端返回 HTML 片段（不是 JSON）
3. HTMX 自动将返回的 HTML 替换到 `#todo-list` 元素

---

## 七、与 Vue 版本的关键区别

### 数据流对比

**Vue 版本**：
```
用户点击 → Vue 方法 → fetch API → JSON 响应 → 更新 data → Vue 重新渲染
```

**HTMX 版本**：
```
用户点击 → HTMX 发送请求 → HTML 片段响应 → HTMX 替换 DOM
```

### 代码位置对比

| 功能 | Vue 版本 | HTMX 版本 |
|------|---------|----------|
| 新增待办 | `app/static/js/app.js` 中的 `saveAdd()` | `routers/todos.py` 中的 `create_todo()` |
| 渲染列表 | Vue 的 `v-for` 指令 | Jinja2 模板 `{% for %}` |
| 切换完成 | `app.js` 中的 `toggleDone()` | `routers/todos.py` 中的 `toggle_done()` |
| 更新页面 | Vue 响应式更新 | HTMX 替换 HTML 片段 |

---

## 八、常见问题

### Q1: 页面刷新后数据丢失

**原因**：HTMX 版本和 Vue 版本使用不同的数据库文件。

**解决**：这是设计如此。`app/` 使用 `todo.db`，`app-1/` 使用 `todo_htmx.db`。

### Q2: 点击待办文字没有反应

**检查**：查看浏览器控制台是否有 JavaScript 错误。

**解决**：确保 HTMX CDN 加载成功：
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

### Q3: 如何调试 HTMX 请求

**方法**：在浏览器开发者工具中：
1. Network 标签查看请求/响应
2. Console 标签执行 `htmx.logAll()` 查看详细日志

### Q4: 与 Vue 版本同时运行会冲突吗

**不会**：两个版本使用不同的端口：
- Vue 版本：http://localhost:8000
- HTMX 版本：http://localhost:8003

可以同时运行，互不影响。

---

## 九、学习建议

### 对比学习法

1. 先完整体验 HTMX 版本的所有功能
2. 再体验 Vue 版本的相同功能
3. 对比两者的代码差异：
   - 同样点击「新增」，代码在哪里？
   - 同样显示列表，数据怎么来的？
   - 同样切换完成，请求怎么发的？

### 思考问题

1. 为什么 HTMX 版本不需要 `app.js`？
2. 为什么 HTMX 版本返回 HTML 而不是 JSON？
3. 什么时候应该用 HTMX，什么时候应该用 Vue？

---

## 十、下一步

完成本版本学习后：

1. **阅读根目录 README.md** - 了解整个项目的架构
2. **对比 Vue 版本代码** - 理解两种实现方式的优劣
3. **尝试添加功能** - 比如搜索、分页、分类
4. **思考演进路径** - 从 HTMX → Vue → 前后端完全分离

---

## 附录

### 文件清单

```
app-1/
├── __init__.py
├── config.py
├── database.py
├── models.py
├── main.py
├── routers/
│   ├── __init__.py
│   └── todos.py
├── static/
│   └── css/style.css
└── templates/
    ├── index.html
    └── partials/
        ├── todo_list.html
        └── edit_form.html
```

共 **10 个代码文件**，全部创建完成后即可运行。

---

> **HTMX 哲学**：
> 
> "The future of web development is not JavaScript. It's HTML."
> 
> —— HTMX 官网
