# From ASP Classic to FastAPI

> FastAPI 版「从 ASP Classic 到现代 Web 开发」进化课程

---

## 项目简介

用**同一个 Todo 应用**，从最原始的 Web 开发方式一路演进到现代前后端分离架构。

**核心理念**：先退化到 ASP Classic 的手感，再掉头进化到现代写法。每一步只变一个维度，不堆砌概念。

---

## 项目结构

```
fromASPClassicToFastAPI/
├── app-6/                   # 第 1 步 — 退无可退（端口 8006）
├── app-5/                   # 第 2 步 — 路由分离（端口 8005）
├── app-2/                   # 第 3 步 — ORM 引入（端口 8002）
├── app-1/                   # 第 4 步 — HTMX 局部刷新（端口 8003）
├── app/                     # 第 5 步 — Vue.js 前后端分离（端口 8000）
├── app+1/                   # 第 6 步 — 前后端彻底分离（端口 8010 + 5173）
├── app+3/                   # 第 7 步 — FastAPI + Nuxt（端口 8012 + 3000）🚧 预告
└── requirements.txt         # 锁定版本的依赖清单
```

> 注：`[Abandon]app1/`、`[Abandon]app2/`、`[Abandon]app3/`、`[Abandon]app4/` 是旧版本，已废弃，不在本轮教学范围内。

---

## 演进路线

```
app-6/  (Mako 模板即路由 + 裸 SQL + 单文件)              ← 退化终点，ASP Classic 手感
  │                                                     Mako 允许模板里写 Python，Jinja2 不允许
  │
  │  模板不写代码，SQL 抽到路由，Mako 换 Jinja2
  ↓
app-5/  (路由分离 + Jinja2 + raw sqlite3)
  │
  │  raw SQL 换成 SQLAlchemy ORM，模板和路由结构不动
  ↓
app-2/  (标准分层 + ORM + 纯 Web 整页刷新)
  │
  │  加 HTMX 属性，返回 HTML 片段替代整页重定向
  ↓
app-1/  (HTMX 局部刷新 + ORM)
  │
  │  后端改 JSON API，前端用 Vue.js CDN 客户端渲染
  ↓
app/    (Vue.js 前后端分离 + Pydantic schemas)
  │
  │  前端从模板剥离成独立 Node.js 工程，加 CORS
  ↓
app+1/  (彻底分离：FastAPI API + Vue/Vite)
  │
  │  Vue/Vite 换成 Nuxt 4，加 SSR + 文件路由 + auto-import
  ↓
app+3/  (FastAPI + Nuxt 4，SSR)                            🚧 预告
```

**设计原则**：每一步只变一个维度。学生先看到问题，再看到解法，不会一次面对太多新概念。

---

## 七版本对比

| | app-6 | app-5 | app-2 | app-1 | app | app+1 | app+3 🚧 |
|---|-------|-------|-------|-------|-----|-------|----------|
| **一句话** | 模板即路由 | 路由分离 | ORM 引入 | 局部刷新 | 前后端分离 | 彻底分离 | Nuxt SSR |
| **模板引擎** | Mako | Jinja2 | Jinja2 | Jinja2 | Jinja2+Vue | 无模板 | 无模板 |
| **数据库访问** | sqlite3 裸 SQL | sqlite3 裸 SQL | SQLAlchemy ORM | SQLAlchemy ORM | SQLAlchemy ORM | SQLAlchemy ORM | SQLAlchemy ORM |
| **前端技术** | 无 | 无 | 无 | HTMX (CDN) | Vue.js (CDN) | Vue+Vite (npm) | Nuxt 4 (npm) |
| **刷新方式** | 整页 | 整页 | 整页 | 局部 | SPA | SPA | SSR+SPA |
| **Pydantic** | 无 | 无 | 无 | 无 | 有 | 有 | 有 |
| **CORS** | 无 | 无 | 无 | 无 | 无 | 有 | 有 |
| **进程数** | 1 | 1 | 1 | 1 | 1 | 2 | 2 |
| **端口** | 8006 | 8005 | 8002 | 8003 | 8000 | 8010+5173 | 8012+3000 |
| **数据库文件** | todo-6.db | todo-5.db | todo-2.db | todo_htmx.db | todo.db | todo+1.db | todo+3.db |
| **模板文件** | 9 个 .mako | 2 个 .html | 2 个 .html | 3 个 .html | 1 个 .html | 0 | 0 |
| **入口文件** | server.py | main.py | main.py | main.py | main.py | backend/main.py | backend/main.py |

---

## 每一步详解

### 第 1 步：app-6/ — 退无可退

Mako 模板引擎，一个 `server.py` 搞定一切。URL 直接映射到模板文件，业务逻辑（Python + SQL）全写在 `.mako` 模板里。这是 ASP Classic / 早期 PHP 时代的真实写法。

> **为什么是 Mako，不是 Jinja2？**
>
> Jinja2 刻意限制了模板能力——只能做变量替换和简单控制流，**不能在模板里写 Python 代码**。Mako 则允许 `<% %>` 标签里写任意 Python，包括 `import sqlite3` 和 `conn.execute()`。这正是 app-6 要呈现的「模板即路由」风格——如果换成 Jinja2，SQL 根本没地方放，只能老老实实写到路由文件里，但那一步是 app-5 的进化任务。

**教学价值**：让学生看到「屎山」——业务逻辑混在模板里是什么体验，建立「为什么需要分离」的痛点认知。同时理解模板引擎的设计哲学差异：Mako 给你全部自由，Jinja2 给你安全边界。

### 第 2 步：app-5/ — 路由分离

SQL 从 9 个 Mako 模板里抽到 `routers/todos.py`，模板换成 Jinja2，从此模板只管渲染 HTML。数据库仍然用 raw sqlite3，SQL 一行没改，只是搬家了。

**教学价值**：关注点分离——模板不写代码、代码不嵌模板。为下一步换 ORM 打好结构基础。

### 第 3 步：app-2/ — ORM 引入

用 SQLAlchemy ORM 替换 raw sqlite3。路由结构、模板、CSS **一字未动**——只换了数据库访问层，界面纹丝不动。

**教学价值**：抽象层的威力——换了底层实现，上层完全无感。学生亲手验证 `conn.execute()` 变成 `db.query(Todo)` 后，页面仍然一模一样。

### 第 4 步：app-1/ — HTMX 局部刷新

不写一行 JavaScript，只给 HTML 加上 `hx-*` 属性，操作后不再整页闪烁。后端从返回 `303 重定向` 变成返回 HTML 片段，HTMX 自动就地替换 DOM。

**教学价值**：零 JS 实现 AJAX 体验——滚动位置不丢、页面不闪、后端改动极小。对比 app-2 的整页刷新，直观感受用户体验差异。

### 第 5 步：app/ — Vue.js 前后端分离

后端不再返回 HTML，改为返回 JSON API（`/api/todos`）。前端用 Vue.js 3 通过 CDN 引入，`fetch` 调用 API 自行渲染。引入 Pydantic schemas 做请求/响应验证。

**教学价值**：从「服务端渲染」到「客户端渲染」的范式转移。理解 RESTful API 设计和 Pydantic 数据验证。

### 第 6 步：app+1/ — 前后端彻底分离

前端从模板剥离成独立 Node.js 工程（Vue + Vite + npm）。后端是纯 API 服务，不渲染 HTML。两个独立进程，通过 CORS 中间件解决跨域。有构建流程、热更新、API 代理。

**教学价值**：从「单体」到「分离部署」的最后一步。npm 生态、Vite 工具链、CORS 跨域——真实项目的样子。

### 第 7 步：app+3/ — Nuxt 4 全栈 🚧 预告

前端从 Vue/Vite 升级到 Nuxt 4。后端 FastAPI 不变，前端获得 SSR（首屏秒开、SEO 友好）、文件系统路由（零配置）、auto-import（少写 import）。同一个 Todo 应用，体验从「白屏等待」到「服务端直出完整 HTML」。

**教学价值**：从「手动搭建前端」到「用前端框架」。理解 CSR vs SSR 的本质差异、Nuxt 的约定优于配置、以及「框架帮你省掉了什么」。

---

## 技术栈（按引入阶段）

### 第 1-2 步（app-6, app-5）

| 组件 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.115.0 | Web 框架 |
| Uvicorn | 0.32.0 | ASGI 服务器 |
| Jinja2 | 3.1.2 | 模板引擎（app-5 引入） |
| Mako | 1.3.9 | 模板引擎（app-6，不在 requirements.txt） |
| python-multipart | 0.0.29 | 表单解析 |

### 第 3-4 步（app-2, app-1）

| 组件 | 版本 | 说明 |
|------|------|------|
| SQLAlchemy | 2.0.36 | ORM（app-2 引入） |
| Pydantic | 2.9.2 | 数据验证（app-2 起有依赖，app/ 正式使用） |
| Starlette | 0.38.6 | ASGI 工具集 |

### 第 5 步（app/）

无新 Python 依赖。Vue.js 3 通过 CDN 引入。

### 第 6 步（app+1/）

| 组件 | 版本 | 说明 |
|------|------|------|
| Vue.js | ^3.5.34 | SPA 框架（npm 管理） |
| Vite | ^8.0.12 | 构建工具 |

### 第 7 步（app+3/）🚧

| 组件 | 版本 | 说明 |
|------|------|------|
| Nuxt | 4.x | 全栈 Vue 框架（SSR/SSG/CSR） |
| @nuxt/ui | — | UI 组件库（待定 v2/v3） |

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

### 运行各版本

```bash
# 第 1 步：退无可退（Mako 模板即路由）
uvicorn app-6.server:app --host 0.0.0.0 --port 8006 --reload

# 第 2 步：路由分离（Jinja2 + raw SQL）
uvicorn app-5.main:app --host 0.0.0.0 --port 8005 --reload

# 第 3 步：ORM 引入（标准分层 + 整页刷新）
uvicorn app-2.main:app --host 0.0.0.0 --port 8002 --reload

# 第 4 步：HTMX 局部刷新
uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload

# 第 5 步：Vue.js 前后端分离
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 第 6 步：前后端彻底分离（两个终端）
# 后端：
uvicorn app+1.backend.main:app --host 0.0.0.0 --port 8010 --reload
# 前端：
cd app+1/frontend && npm run dev

# 第 7 步：FastAPI + Nuxt 🚧（两个终端）
# 后端：
uvicorn app+3.backend.main:app --host 0.0.0.0 --port 8012 --reload
# 前端：
cd app+3/frontend && npm run dev
```

---

## 各项目详细文档

| 版本 | 文档 | 核心变化 |
|------|------|---------|
| app-6/ | [app-6/README.md](app-6/README.md) | 退无可退 — 模板即路由 + 裸 SQL |
| app-5/ | [app-5/README.md](app-5/README.md) | 路由分离 — SQL 搬家 + Mako→Jinja2 |
| app-2/ | [app-2/README.md](app-2/README.md) | ORM 引入 — raw SQL→SQLAlchemy |
| app-1/ | [app-1/README.md](app-1/README.md) | HTMX — 零 JS 局部刷新 |
| app/ | [app/README.md](app/README.md) | Vue.js — 前后端分离 |
| app+1/ | [app+1/README.md](app+1/README.md) | 彻底分离 — FastAPI + Vue/Vite |
| app+3/ 🚧 | [app+3/README.md](app+3/README.md) | Nuxt 4 — SSR + 文件路由 + auto-import |

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
