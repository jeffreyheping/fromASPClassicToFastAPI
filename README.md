# From ASP Classic to FastAPI

> FastAPI 版「从 ASP Classic 到现代 Web 开发」进化课程

---

## 项目简介

本项目是 [fromASPClassicToPy4web](https://github.com/jeffreyheping/fromASPClassicToPy4web) 的 FastAPI 移植版本，用同一个 Todo 应用演示从传统 Web 开发到现代前后端分离 + 认证 + 测试的完整演进路径。

**核心理念**：先退化到 ASP Classic 的手感，再掉头进化到现代写法。

---

## 项目结构

```
fromASPClassicToFastAPI/
├── app/                     # 阶段 1 — Vue.js 前后端分离（端口 8000）
├── app-1/                   # 阶段 1 — HTMX 服务端渲染（端口 8003）
├── app1/                    # 阶段 2 — 双 UI 合并（端口 8005）
├── app3/                    # 阶段 3 — 双 UI + OAuth2 认证（端口 8007）
├── app4/                    # 阶段 4 — 双 UI + OAuth2 认证 + 测试（端口 8008）
├── requirements.txt         # 锁定版本的依赖清单
└── README.md                # 本文件
```

---

## 演进路线

```
app/ (Vue SPA)  ──┐
                  ├─→ app1/ (双 UI 合并，无认证)
app-1/ (HTMX)  ──┘        │
                           ↓
                    app3/ (双 UI + OAuth2 认证)
                           │
                           ↓
                    app4/ (双 UI + OAuth2 + pytest 测试)
```

---

## 五个版本对比

| | app/ | app-1/ | app1/ | app3/ | app4/ |
|---|------|--------|-------|-------|-------|
| **架构** | 前后端分离 | 服务端渲染 | 双 UI 合并 | 双 UI + 认证 | 双 UI + 认证 + 测试 |
| **前端** | Vue.js 3 | HTMX | Vue + HTMX | Vue + HTMX | Vue + HTMX |
| **认证** | 无 | 无 | 无 | OAuth2 JWT + Session | OAuth2 JWT + Session |
| **测试** | 无 | 无 | 无 | 无 | pytest（23 项） |
| **端口** | 8000 | 8003 | 8005 | 8007 | 8008 |
| **数据库** | todo.db | todo_htmx.db | todo_api.db | todo3.db | todo4.db |

### 阶段 1：独立项目（app/ & app-1/）

两个独立项目，业务逻辑各自拷贝一份。展示前后端分离的「最终形态」和 HTMX 的「极简方案」。

| 特性 | app/ (Vue.js) | app-1/ (HTMX) |
|------|---------------|---------------|
| 数据格式 | JSON API | HTML 片段 |
| 学习曲线 | 需学习 Vue 概念 | 只需 HTML 属性 |
| 适用场景 | 复杂交互应用 | 教学过渡、简单 CRUD |

**教学价值**：对比同一功能在两种范式下的实现差异。

### 阶段 2：合并共享层（app1/）

把 app/ 和 app-1/ 合并成一个项目，共享同一套 services/database/models。用文件夹结构演示「关注点分离」——Vue 和 HTMX 只在自己的 router 层不同，底层完全共享。

**核心变化**：
- 抽离 `core/services.py`（6 个纯函数，零 HTTP 依赖）
- `routers/api/` 返回 JSON，`routers/web/` 返回 HTML 片段
- CSS 拆分为 base.css + app.css + internal.css
- 用 `Path(__file__).resolve()` 替代硬编码相对路径

### 阶段 3：加入认证（app3/）

在 app1 的基础上加入完整的认证体系。Vue 端采用 OAuth2 标准 JWT 认证，HTMX 端采用 Session 认证，Swagger UI 原生支持一键登录。

**核心特性**：
- OAuth2PasswordBearer + python-jose JWT
- 角色分流：guest → Vue 端，staff → HTMX 端
- 401 未登录时浏览器自动重定向到登录页
- Swagger UI 自动显示 🔒 图标

### 阶段 4：加入测试（app4/）

在 app3 的基础上增加完整的自动化测试体系，展示如何让现有代码「可测试」——只改最少的东西（配置环境变量 + 工厂函数），不动业务逻辑。

**核心变化**：
- `config.py` 支持环境变量覆盖
- `main.py` 改为 `create_app()` 工厂函数
- 23 个 pytest 测试（services 层 + API 层）
- in-memory SQLite + `dependency_overrides` 实现测试隔离

---

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

### 运行各阶段

```bash
# 阶段 1 — Vue 版本
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 阶段 1 — HTMX 版本
uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload

# 阶段 2 — 双 UI 合并
uvicorn app1.main:app --host 0.0.0.0 --port 8005 --reload

# 阶段 3 — 双 UI + 认证
uvicorn app3.main:app --host 0.0.0.0 --port 8007 --reload

# 阶段 4 — 双 UI + 认证 + 测试
uvicorn app4.main:app --host 0.0.0.0 --port 8008 --reload
```

### 运行测试（app4 专属）

```bash
pytest app4/tests/ -v
```

---

## 技术栈（版本已锁定）

| 组件 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.115.0 | Web 框架 |
| Uvicorn | 0.32.0 | ASGI 服务器 |
| SQLAlchemy | 2.0.36 | ORM |
| Pydantic | 2.9.2 | 数据验证 |
| Jinja2 | 3.1.2 | 模板引擎 |
| python-jose | 3.5.0 | JWT 生成/验证（app3/app4） |
| pytest | — | 测试框架（app4） |
| Vue.js 3 | CDN | SPA 前端 |
| HTMX | 1.9.10 | 局部刷新 |

---

## 教学价值

每条线的跨度都不大，但每步都踩在特定的教学点上：

1. **app/ → app-1/**：同一功能，两种范式（JSON API vs HTML 片段）
2. **app + app-1 → app1/**：「为什么重复代码是坏味道」→ 抽离共享层
3. **app1 → app3/**：「无认证的应用不是真实应用」→ OAuth2 + Session
4. **app3 → app4/**：「没有测试的代码不能放心改」→ pytest + 工厂函数

---

## 各项目详细文档

| 版本 | 文档 | 核心主题 |
|------|------|---------|
| app/ | [app/README.md](app/README.md) | Vue.js 前后端分离入门 |
| app-1/ | [app-1/README.md](app-1/README.md) | HTMX 局部刷新入门 |
| app1/ | [app1/README.md](app1/README.md) | 分层架构与代码复用 |
| app3/ | [app3/README.md](app3/README.md) | OAuth2 JWT + Session 双认证 |
| app4/ | [app4/README.md](app4/README.md) | pytest 测试 + 工厂函数 |

---

## 致谢

- [jeffreyheping](https://github.com/jeffreyheping) — 原 py4web 进化课程作者
- [Sebastián Ramírez](https://github.com/tiangolo) — FastAPI 作者
- [HTMX](https://htmx.org/) — 极简的交互设计哲学

---

## 许可证

MIT License

---

> "先退化到 ASP Classic 的手感，再掉头进化到现代写法。"
>
> —— jeffreyheping
