# FastAPI 接口设计：Vue vs HTMX 对比

> 理解前后端分离 vs 服务端渲染的本质差异

---

## 一句话总结

| 前端方式 | FastAPI 返回什么 | 核心差异 |
|---------|-----------------|---------|
| **Vue.js** | JSON 数据 | 后端给数据，前端负责渲染 |
| **HTMX** | HTML 片段 | 后端直接渲染好，前端负责替换 |

---

## 代码对比：获取待办列表

### Vue 版本 - 返回 JSON

```python
@router.get("", response_model=List[TodoSchema])
def get_todos(db: Session = Depends(get_db)):
    """获取所有待办事项"""
    return db.query(Todo).order_by(Todo.id.desc()).all()
```

**请求**：`GET /api/todos`

**响应**：
```json
[
  {"id": 2, "info": "学习 FastAPI", "status": 0},
  {"id": 1, "info": "完成课程", "status": 1}
]
```

**谁渲染页面**：Vue.js 在前端用 `v-for` 把 JSON 变成 HTML

---

### HTMX 版本 - 返回 HTML 片段

```python
@router.get("/list")
def get_todo_list(request: Request, db: Session = Depends(get_db)):
    """获取待办列表片段"""
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })
```

**请求**：`GET /todos/list`

**响应**：
```html
<ul class="todo-list">
  <li><span>学习 FastAPI</span> <button>✏️</button> <button>🗑️</button></li>
  <li class="done"><span>完成课程</span> <button>✏️</button> <button>🗑️</button></li>
</ul>
```

**谁渲染页面**：FastAPI 在后端用 Jinja2 模板渲染好，HTMX 直接替换到页面上

---

## 代码对比：新增待办

### Vue 版本 - JSON API

```python
@router.post("", response_model=TodoSchema, status_code=status.HTTP_201_CREATED)
def create_todo(todo_in: TodoCreate, db: Session = Depends(get_db)):
    """新增待办事项"""
    todo = Todo(info=todo_in.info)
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo
```

**前端代码**（`app/static/js/app.js`）：
```javascript
async saveAdd() {
    const res = await fetch('/api/todos', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ info: this.form.info })
    });
    const newTodo = await res.json();
    this.todos.unshift(newTodo);
    this.view = 'list';
}
```

---

### HTMX 版本 - 表单处理

```python
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

    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })
```

**前端代码**（HTML 属性）：
```html
<form hx-post="/todos"
      hx-target="#todo-list"
      hx-swap="innerHTML"
      hx-on::after-request="this.reset()">
    <input type="text" name="info" placeholder="输入待办事项..." required>
    <button type="submit">+ 新增</button>
</form>

<div id="todo-list">
    {% include "partials/todo_list.html" %}
</div>
```

**不需要 JavaScript 代码！**

---

## 关键差异对比表

| 方面 | Vue 版本 | HTMX 版本 |
|------|---------|----------|
| **路由文件** | `app/routers/todos.py` | `app-1/routers/todos.py` |
| **路由前缀** | `/api/todos` | `/todos` |
| **请求方法** | `POST /api/todos` | `POST /todos` |
| **请求体格式** | JSON: `{"info": "xxx"}` | 表单: `info=xxx` |
| **接收参数** | `todo_in: TodoCreate` | `info: str = Form(...)` |
| **响应格式** | JSON: `{"id": 1, ...}` | HTML: `<ul>...</ul>` |
| **Pydantic 模型** | ✅ 需要定义 | ❌ 不需要 |
| **错误处理** | 返回 JSON 错误 | 返回错误页面或片段 |
| **前端代码** | JavaScript (fetch) | HTML 属性 (hx-*) |
| **渲染位置** | 前端 (Vue) | 后端 (Jinja2) |

---

## 数据流对比

### Vue 版本 - 前后端分离

```
┌─────────────┐     GET /api/todos      ┌─────────────┐
│             │ ──────────────────────→ │             │
│   Vue.js    │                         │   FastAPI   │
│   (浏览器)   │ ←────────────────────── │   (服务器)   │
│             │    JSON: [{id:1,...}]   │             │
└─────────────┘                         └─────────────┘
       │
       │ v-for 渲染
       ↓
┌─────────────┐
│   <ul>      │
│   <li>...</li>│
│   </ul>     │
└─────────────┘
```

**特点**：
- 后端只给数据，不管怎么显示
- 前端负责所有界面逻辑
- 前后端通过 JSON 通信

---

### HTMX 版本 - 服务端渲染

```
┌─────────────┐     GET /todos/list     ┌─────────────┐
│             │ ──────────────────────→ │             │
│   HTMX      │                         │   FastAPI   │
│   (浏览器)   │ ←────────────────────── │   (服务器)   │
│             │    HTML: <ul>...</ul>   │             │
└─────────────┘                         └─────────────┘
       │
       │ hx-swap="innerHTML"
       ↓
┌─────────────┐
│  直接替换    │
│  DOM 元素    │
└─────────────┘
```

**特点**：
- 后端渲染好完整的 HTML
- 前端只负责替换 DOM
- 通信的是 HTML 片段，不是 JSON

---

## 为什么 HTMX 更适合教学

### 1. 可见性

| Vue 版本 | HTMX 版本 |
|---------|----------|
| 网络请求隐藏在 Vue 内部 | `hx-post` 属性直接写在 HTML 上 |
| 需要打开 DevTools 才能看到请求 | 一眼就能看到请求发到哪里 |
| JSON 数据需要格式化才能读 | HTML 片段直接在响应里 |

### 2. 概念简单

**Vue 需要理解**：
- 响应式数据 (`data`, `ref`)
- 生命周期 (`mounted`, `updated`)
- 异步编程 (`async/await`)
- JSON 解析

**HTMX 只需要理解**：
- 点击按钮 → 发送请求 → 替换 HTML
- 就像普通的表单提交，只是不刷新整个页面

### 3. 渐进式学习

```
阶段 1: 普通表单（整页刷新）
   ↓
阶段 2: HTMX（局部刷新，后端渲染）
   ↓ 理解 AJAX 本质后
阶段 3: Vue（局部刷新，前端渲染）
   ↓ 理解组件化后
阶段 4: 前后端完全分离
```

---

## 什么时候用什么

### 用 HTMX 的场景

- ✅ 教学演示 AJAX 原理
- ✅ 简单的 CRUD 应用
- ✅ 团队不熟悉 JavaScript
- ✅ 需要快速原型
- ✅ SEO 要求高（服务端渲染）

### 用 Vue 的场景

- ✅ 复杂的交互逻辑
- ✅ 需要离线功能（PWA）
- ✅ 大量实时数据更新
- ✅ 需要复用组件
- ✅ 团队熟悉现代前端开发

---

## 总结

| 问题 | 答案 |
|------|------|
| FastAPI 的代码变了吗？ | 变了，从返回 JSON 变成返回 HTML |
| 接口设计变了吗？ | 变了，从 RESTful API 变成服务端渲染路由 |
| 工作量变了吗？ | HTMX 版本后端工作量增加（要渲染模板），前端工作量减少（不用写 JS） |
| 性能变了吗？ | HTMX 首屏更快（服务端渲染），但传输数据更大（HTML vs JSON） |
| 维护变了吗？ | HTMX 版本逻辑更集中（都在后端），Vue 版本前后端逻辑分散 |

**核心洞察**：

HTMX 不是「退化」，而是「回归本源」。它让孩子们看到：
- AJAX 不是魔法，就是 HTTP 请求
- 局部刷新不是框架特性，就是 DOM 操作
- 前后端分离不是唯一选择，服务端渲染依然有用

理解了这些，再学 Vue/React 时，就知道框架解决的是什么问题了。
