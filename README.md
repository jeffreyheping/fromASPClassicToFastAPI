# From ASP Classic to FastAPI

> FastAPI 版「从 ASP Classic 到现代 Web 开发」进化课程

---

## 项目简介

本项目是 [fromASPClassicToPy4web](https://github.com/jeffreyheping/fromASPClassicToPy4web) 的 FastAPI 移植版本，用同一个 Todo 应用演示从传统 Web 开发到现代前后端分离的完整演进路径。

**核心理念**：先退化到 ASP Classic 的手感，再掉头进化到现代写法。

---

## 项目结构

```
fromASPClassicToFastAPI/
├── app-6/                   # 退无可退 — 最原始 Web 开发（端口 8006）
├── app-5/                   # 路由分离 — 代码开始分层（计划中）
├── app-4/                   # ORM 引入 — 告别裸 SQL（计划中）
├── app-2/                   # 现代基础 — 标准分层架构（端口 8002）
├── app-1/                   # HTMX 局部刷新（端口 8003）
├── app/                     # Vue.js 前后端分离（端口 8000）
├── app+1/                   # 前后端彻底分离（端口 8008）
├── requirements.txt         # 锁定版本的依赖清单
└── README.md                # 本文件
```

> **注**：app1、app3、app4 已放弃，不再维护。

---

## 演进路线

### 已完成

```
app-6/  (Mako 模板即路由 + 裸 SQL)     ← 退化终点，ASP Classic 手感
  ↓
app-5/  (路由分离，模板不写代码)        ← 计划中
  ↓
app-4/  (SQLAlchemy ORM + Jinja2)      ← 计划中
  ↓
app-2/  (标准分层：config/database/models/routers)
  ↓
app-1/  (HTMX，局部刷新)
  ↓
app/    (Vue.js，前后端分离)
  ↓
app+1/  (前后端彻底分离：FastAPI + Vue/Vite)
```

### 各版本对比

| | app-6/ | app-2/ | app-1/ | app/ | app+1/ |
|---|--------|--------|--------|------|--------|
| **架构** | 模板即路由 | 标准分层 | HTMX 局部刷新 | 前后端分离 | 彻底分离 |
| **模板引擎** | Mako | Jinja2 | Jinja2 | Jinja2 (CDN Vue) | Vue + Vite |
| **数据库** | sqlite3 裸 SQL | SQLAlchemy ORM | SQLAlchemy ORM | SQLAlchemy ORM | SQLAlchemy ORM |
| **认证** | 无 | 无 | 无 | 无 | 无 |
| **端口** | 8006 | 8002 | 8003 | 8000 | 8010 |
| **数据库文件** | todo-6.db | todo-2.db | todo_htmx.db | todo.db | todo+1.db |

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

### 运行各版本

```bash
# app-6 — 退无可退版（最原始）
uvicorn app-6.server:app --host 0.0.0.0 --port 8006 --reload

# app-2 — 标准分层版
uvicorn app-2.main:app --host 0.0.0.0 --port 8002 --reload

# app-1 — HTMX 版
uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload

# app — Vue.js 版
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# app+1 — 前后端彻底分离
# 后端
uvicorn app+1.backend.main:app --host 0.0.0.0 --port 8009 --reload
# 前端
cd app+1/frontend && npm run dev
```

---

## 各项目详细文档

| 版本 | 文档 | 核心主题 |
|------|------|---------|
| app-6/ | [app-6/README.md](app-6/README.md) | 退无可退 — Mako 模板即路由 + 裸 SQL |
| app-2/ | [app-2/README.md](app-2/README.md) | 标准分层 — config/database/models/routers |
| app-1/ | [app-1/README.md](app-1/README.md) | HTMX — 零 JS 局部刷新 |
| app/ | [app/README.md](app/README.md) | Vue.js — 前后端分离 |
| app+1/ | [app+1/README.md](app+1/README.md) | 彻底分离 — FastAPI + Vue/Vite |

---

## 致谢

- [jeffreyheping](https://github.com/jeffreyheping) — 原 py4web 进化课程作者
- [Sebastián Ramírez](https://github.com/tiangolo) — FastAPI 作者

---

## 许可证

MIT License

---

> "先退化到 ASP Classic 的手感，再掉头进化到现代写法。"
>
> —— jeffreyheping
