# Todo FastAPI — 双 UI 架构（app2版本）

> FastAPI 版「从 ASP Classic 到前后端分离」进化课程 - app2版本（独立数据库）

---

## 项目简介

这是 `app1/` 的复制版本，用于演示登录注册功能。与 `app1/` 的区别仅在于数据库文件名不同（`todo2.db`），代码完全同源。

| 访问方 | URL | 前端技术 | 数据交互 |
|--------|-----|---------|---------|
| 外部客人 | `/` | Vue.js 3 SPA | JSON API (`/api/todos`) |
| 内部员工 | `/internal` | HTMX + Jinja2 模板 | HTML 片段 (`/todos`) |

---

## 与 app1 的区别

| 项目 | 数据库文件 | 用途 |
|------|-----------|------|
| `app1/` | `todo_api.db` | 双 UI 架构演示 |
| `app2/` | `todo2.db` | 登录注册功能演示 |

**代码层面**：`app2/` 是 `app1/` 的完整复制，仅修改了 `core/config.py` 中的数据库路径和 `main.py` 的标题。

---

## 技术栈

与 `app1/` 完全相同：

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.115.0 |
| 数据库 | SQLite + SQLAlchemy | 2.0.36 |
| 数据验证 | Pydantic | 2.9.2 |
| 模板引擎 | Jinja2 | 3.1.2 |
| ASGI 服务器 | Uvicorn | 0.32.0 |
| 外部 UI | Vue.js 3 + Options API | 最新版 (CDN) |
| 内部 UI | HTMX | 1.9.10 (CDN) |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r ../requirements.txt --break-system-packages
```

### 2. 运行项目

```bash
uvicorn app2.main:app --host 0.0.0.0 --port 8006 --reload
```

### 3. 访问应用

| 页面 | 地址 |
|------|------|
| Vue 版（外部客人） | http://localhost:8006 |
| HTMX 版（内部员工） | http://localhost:8006/internal |
| API 文档 | http://localhost:8006/docs |

---

## 项目结构

与 `app1/` 相同：

```
app2/
├── __init__.py
├── main.py                     # 入口（标题改为 app2）
├── core/
│   ├── __init__.py
│   ├── config.py               # 数据库改为 todo2.db
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── routers/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── todos.py
│   └── web/
│       ├── __init__.py
│       └── todos.py
├── templates/
│   ├── index.html
│   ├── internal.html
│   └── partials/
├── static/
│   ├── js/app.js
│   └── css/
└── README.md                   # 本文件
```

---

## 说明

`app2/` 是为了在不影响 `app1/` 的情况下，演示登录注册功能而创建的。两个项目代码同源，可以对比学习：

- `app1/` — 基础双 UI 架构
- `app2/` — 在双 UI 架构基础上增加登录注册

---

## 许可证

MIT License
