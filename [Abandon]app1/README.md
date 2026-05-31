# Todo FastAPI — 双 UI 架构

> FastAPI 版「从 ASP Classic 到前后端分离」进化课程 - 合并版

---

## 项目简介

这是一个基于 **FastAPI** 的待办事项应用，同时对外部客人和内部员工提供两套不同的前端界面，但共享同一套后端业务逻辑。

| 访问方 | URL | 前端技术 | 数据交互 |
|--------|-----|---------|---------|
| 外部客人 | `/` | Vue.js 3 SPA | JSON API (`/api/todos`) |
| 内部员工 | `/internal` | HTMX + Jinja2 模板 | HTML 片段 (`/todos`) |

### 为什么做这个版本

`app/` (Vue 版) 和 `app-1/` (HTMX 版) 是两个独立的项目，虽然业务逻辑完全相同，代码却是两份拷贝。这样既不利于维护，也不利于教学——孩子们会困惑：改了 Vue 版的 bug，HTMX 版怎么还在？

这个版本证明了一件事：**同一套 FastAPI，可以同时服务 JSON API 和 HTML 片段两种消费者**。关键是读懂方方的区别在哪、共享在哪。

---

## 技术栈（版本已锁定）

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.115.0 |
| 数据库 | SQLite + SQLAlchemy | 2.0.36 |
| 数据验证 | Pydantic | 2.9.2 |
| 模板引擎 | Jinja2 | 3.1.2 |
| ASGI 服务器 | Uvicorn | 0.32.0 |
| 外部 UI | Vue.js 3 + Options API | 最新版 (CDN) |
| 内部 UI | HTMX | 1.9.10 (CDN) |
| 样式 | 原生 CSS（分层） | - |

---

## 项目结构

```
app1/
├── __init__.py
├── main.py                     # 入口 · 挂载两套路由
├── core/                       # 共享层 —— 不依赖 HTTP
│   ├── __init__.py
│   ├── config.py               # 数据库 URI 配置
│   ├── database.py             # SQLAlchemy 引擎 + 会话管理
│   ├── models.py               # Todo ORM 模型
│   ├── schemas.py              # Pydantic 请求/响应验证
│   └── services.py             # 纯业务逻辑（6 个函数，无 HTTP 依赖）
├── routers/
│   ├── __init__.py
│   ├── api/                    # JSON API —— 给 Vue 用
│   │   ├── __init__.py
│   │   └── todos.py            # 返回 JSON，调用 core/services
│   └── web/                    # HTML 片段 —— 给 HTMX 用
│       ├── __init__.py
│       └── todos.py            # 返回 HTML 片段，调用 core/services
├── templates/
│   ├── index.html              # Vue SPA 入口（外部客人）
│   ├── internal.html           # HTMX 管理页（内部员工）
│   └── partials/
│       ├── todo_list.html      # 待办列表片段
│       └── edit_form.html      # 编辑表单片段
├── static/
│   ├── js/app.js               # Vue.js 3 前端逻辑
│   └── css/
│       ├── base.css            # 两套 UI 共享样式
│       ├── app.css             # Vue SPA 专用
│       └── internal.css        # HTMX 专用
└── README.md                   # 本文件
```

### 结构设计原则

```
外部客人 → /      → Vue.js SPA  → /api/todos (JSON)     ← routers/api/
内部员工 → /internal → HTMX 页面  → /todos    (HTML 片段) ← routers/web/
                                    ↑
                              都调 core/services
```

- **`core/`** — 零 HTTP 依赖。纯 Python 函数，不知道什么是 Request、Response、模板。
- **`routers/api/`** — 唯一的职责：接收 HTTP 请求 → 调 services → 返回 JSON。
- **`routers/web/`** — 唯一的职责：接收 HTTP 请求 → 调 services → 返回 HTML 片段。
- **`templates/`** — Jinja2 模板，`index.html` 给 Vue 用，`internal.html` 给 HTMX 用。
- **`static/css/`** — 拆分为三层：`base.css`（共享）、`app.css`（Vue 专用）、`internal.css`（HTMX 专用）。

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r ../requirements.txt --break-system-packages
```

### 2. 运行项目

```bash
cd C:\Users\jeffr\Documents\GitHub\fromASPClassicToFastAPI
"C:\Users\jeffr\anaconda3\python.exe" -m uvicorn app1.main:app --host 0.0.0.0 --port 8005 --reload
```

### 3. 访问应用

| 页面 | 地址 |
|------|------|
| Vue 版（外部客人） | http://localhost:8005 |
| HTMX 版（内部员工） | http://localhost:8005/internal |
| API 文档 | http://localhost:8005/docs |

---

## 路由一览

### JSON API（给 Vue 用）

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/api/todos` | 获取所有待办 |
| POST | `/api/todos` | 新增待办 |
| GET | `/api/todos/{id}` | 获取单个待办 |
| PUT | `/api/todos/{id}` | 更新待办内容 |
| PUT | `/api/todos/{id}/toggle` | 切换完成状态 |
| DELETE | `/api/todos/{id}` | 删除待办 |

### HTML 片段（给 HTMX 用）

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/todos/list` | 渲染列表片段 |
| POST | `/todos` | 新增待办 → 返回列表 |
| GET | `/todos/{id}/edit` | 返回编辑表单 |
| PUT | `/todos/{id}` | 更新内容 → 返回列表 |
| PUT | `/todos/{id}/toggle` | 切换完成 → 返回列表 |
| DELETE | `/todos/{id}` | 删除待办 → 返回列表 |

---

## 核心设计决策

### 为什么两套 UI 共享同一个 services 层？

`app/` 和 `app-1/` 的业务逻辑是两份一样的代码，改一处要同步另一处。把逻辑抽到 `core/services.py` 里（6 个纯函数），两个 router 各自调用，只在自己的路由函数里决定「返回 JSON 还是 HTML」。

```python
# services.py —— 不知道 HTTP 是什么
def get_all(db: Session) -> list[Todo]:
    return db.query(Todo).order_by(Todo.status, Todo.id.desc()).all()

def toggle_status(db: Session, todo_id: int) -> Todo | None:
    # ...纯业务逻辑
```

```python
# routers/api/todos.py —— 返回 JSON
@router.get("/", response_model=list[schemas.TodoOut])
def list_todos(db: Session = Depends(get_db)):
    return services.get_all(db)  # Pydantic 自动序列化

# routers/web/todos.py —— 返回 HTML
@router.get("/list")
def list_todos(request: Request, db: Session = Depends(get_db)):
    todos = services.get_all(db)
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request, "todos": todos,
    })
```

### 为什么 CSS 拆成三个文件？

`base.css` 放两套 UI 都用的东西（reset、按钮、列表），`app.css` 和 `internal.css` 各自放专属样式。理由：

- **意图清晰** — 一眼看出哪些是共享的、哪些是各管各的
- **互不干扰** — 改 Vue 表单不会意外影响 HTMX 页面
- **教学价值** — 展示「关注点分离」不止适用于代码，也适用于样式

### 为什么路径用 `Path(__file__).resolve()` 而不是相对路径？

`app/` 和 `app-1/` 的模板和数据库路径都用了硬编码的相对路径（`"app/templates"`、`"./todo.db"`），这依赖启动时的当前工作目录。从项目根目录启动没问题，换个目录就炸。

`app1` 全部使用 `Path(__file__).resolve()` 计算绝对路径，**位置无关**——不管从哪里启动 uvicorn，都能找到正确的模板和数据库。

### 数据库为什么放在项目根目录？

`todo_api.db` 放在 `fromASPClassicToFastAPI/` 目录下，和 `todo.db`（app 用）、`todo_htmx.db`（app-1 用）平级。这样三个项目的数据库文件集中管理，不会被各自的项目目录散落。

---

## 与原有项目的关系

```
app/        Vue.js 版      —— 独立项目，未改动
app-1/      HTMX 版        —— 独立项目，未改动
app1/       双 UI 合并版    —— 新建，合并了两者的代码
```

`app1/` 不是替代 `app/` 和 `app-1/`，而是演示「如何合并」的第三个教学项目。原有两个项目保持原样，作为对比参考。

### 代码溯源

| app1 文件 | 来源 |
|-----------|------|
| `core/models.py` | `app/models.py`（两个项目的 models 完全相同） |
| `core/database.py` | `app/database.py`（两个项目的 database 完全相同） |
| `core/schemas.py` | `app/schemas.py` |
| `core/services.py` | 从 `app/routers/todos.py` 和 `app-1/routers/todos.py` 的业务逻辑抽离 |
| `core/config.py` | 新建（原来两个 config 只是两行 URI 常量） |
| `routers/api/todos.py` | `app/routers/todos.py`（去掉业务逻辑，只留 HTTP 层） |
| `routers/web/todos.py` | `app-1/routers/todos.py`（去掉业务逻辑，只留 HTTP 层） |
| `templates/index.html` | `app/templates/index.html`（不变） |
| `templates/internal.html` | `app-1/templates/index.html`（改名） |
| `templates/partials/` | `app-1/templates/partials/`（不变） |
| `static/js/app.js` | `app/static/js/app.js`（不变） |
| `static/css/base.css` | 从两个 style.css 提取共享部分 |
| `static/css/app.css` | 从 `app/static/css/style.css` 提取 Vue 专用部分 |
| `static/css/internal.css` | 从 `app-1/static/css/style.css` 提取 HTMX 专用部分 |

---

## 尚未实现

- **认证** — 外部客人和内部员工目前没有权限隔离，任何人都能访问任意页面。认证逻辑需要从长计议。

---

## 教学价值

### 孩子们能学到什么

1. **关注点分离** — services 层不碰 HTTP，router 层不碰业务逻辑，CSS 也分层
2. **一个后端，多种前端** — 同样的业务逻辑，可以服务 JSON API（给前端框架）和 HTML 片段（给 HTMX/传统多页应用）
3. **路径健壮性** — `Path(__file__).resolve()` vs 硬编码相对路径，为什么前者是工业级写法
4. **架构演进** — 从两个独立项目到合并为一个，理解「什么时候该共享、什么时候该分离」

### 学习路径

```
阶段1: app/   (Vue.js 前后端分离)     → 理解 SPA 和 JSON API
阶段2: app-1/ (HTMX 服务端渲染)       → 理解局部刷新和 HTML 片段
阶段3: app1/  (双 UI 合并)           → 理解分层架构和代码复用
```

---

## 致谢

- [jeffreyheping](https://github.com/jeffreyheping) — 原 py4web 进化课程作者
- [FastAPI](https://fastapi.tiangolo.com/) — 现代 Python Web 框架
- [HTMX](https://htmx.org/) — 极简的交互设计哲学

---

## 许可证

MIT License

---

> "外部看门面，内部看效率。一个后端，两种前脸。"
