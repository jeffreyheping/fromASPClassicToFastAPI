# Todo FastAPI — 双认证架构（app2版本）

> FastAPI 版「JWT + Session 双认证」教学项目 - 从零手写认证系统

---

## 项目简介

`app2/` 演示**手写认证系统**：不依赖第三方认证库，从零实现 JWT（Vue版）和 Session（HTMX版）两套认证机制。

| 访问方 | URL | 前端技术 | 认证方式 | 数据交互 |
|--------|-----|---------|---------|---------|
| 外部客人 | `/` | Vue.js 3 SPA | **JWT** (Bearer Token) | JSON API (`/api/todos`) |
| 内部员工 | `/internal` | HTMX + Jinja2 | **Session** (Cookie) | HTML 片段 (`/todos`) |

**核心特性：**
- 统一用户表，支持角色控制（guest/staff）
- 注册默认 role=guest，需手动改数据库升级为 staff
- 两套认证完全隔离，各自注册各自登录

---

## 与 app1 的区别

| 项目 | 数据库 | 核心差异 |
|------|--------|---------|
| `app1/` | `todo_api.db` | 基础双 UI，无认证 |
| `app2/` | `todo2.db` | **手写 JWT + Session 认证** |

---

## 认证机制详解

### Vue 版 — JWT 认证

```
登录 → POST /api/auth/login → 返回 {access_token, user}
请求 → Header: Authorization: Bearer <token>
验证 → 自定义 get_current_user_jwt() 解析 token
```

**特点：**
- Token 存储在 localStorage
- 前端控制登录后跳转
- Swagger 需手动输入 token

### HTMX 版 — Session 认证

```
登录 → POST /auth/login → 设置 session cookie
请求 → 浏览器自动带 cookie
验证 → 自定义 get_current_user_session() 读取 session
跳转 → 后端控制：guest→/, staff→/internal
```

**特点：**
- 传统服务端渲染模式
- 浏览器自动处理 cookie
- 退出即清除 session

---

## 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 后端框架 | FastAPI | 0.115.0 | Web 框架 |
| 数据库 | SQLite + SQLAlchemy | 2.0.36 | 数据持久化 |
| 密码哈希 | SHA256 | - | 教学用（生产请用 bcrypt） |
| JWT 处理 | python-jose | 3.5.0 | Token 生成/验证 |
| Session | Starlette SessionMiddleware | - | HTMX 版认证 |
| 外部 UI | Vue.js 3 | 最新 CDN | SPA 前端 |
| 内部 UI | HTMX | 1.9.10 | 服务端渲染 |

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

| 页面 | 地址 | 说明 |
|------|------|------|
| Vue 版 | http://localhost:8006 | 外部客人入口 |
| HTMX 版 | http://localhost:8006/internal | 内部员工入口（需登录） |
| API 文档 | http://localhost:8006/docs | Swagger UI |

### 4. 测试认证流程

**Vue 版：**
1. 打开 http://localhost:8006
2. 点击「注册」创建账号（默认 guest）
3. 登录后使用 Todo 功能

**HTMX 版：**
1. 打开 http://localhost:8006/auth/login
2. 登录后根据角色自动跳转
3. staff 可访问 /internal，guest 跳回首页

**升级 staff：**
```bash
sqlite3 todo2.db "UPDATE users SET role='staff' WHERE username='你的用户名';"
```

---

## 项目结构

```
app2/
├── main.py                     # 入口，Session 中间件配置
├── core/
│   ├── config.py               # 数据库配置（todo2.db）
│   ├── security.py             # JWT + Session 认证工具
│   ├── models.py               # User + Todo 模型
│   └── services.py             # 业务逻辑
├── routers/
│   ├── api/                    # Vue 版 API 路由
│   │   ├── auth.py             # JWT 登录/注册
│   │   └── todos.py            # Todo CRUD（需 JWT）
│   └── web/                    # HTMX 版 Web 路由
│       ├── auth.py             # Session 登录/注册
│       └── todos.py            # Todo CRUD（需 Session）
├── templates/                  # Jinja2 模板
├── static/                     # CSS/JS
└── README.md
```

---

## 核心代码对比

| 功能 | Vue 版 | HTMX 版 |
|------|--------|---------|
| 登录端点 | `POST /api/auth/login` | `POST /auth/login` |
| 参数格式 | JSON | Form |
| 认证依赖 | `get_current_user_jwt` | `get_current_user_session` |
| 用户信息 | 前端存 localStorage | 后端存 session |

---

## 学习要点

1. **JWT 原理**：token 生成、验证、Bearer 传输
2. **Session 原理**：cookie、session 中间件、服务端存储
3. **双认证并存**：同一用户表，两套认证机制
4. **角色控制**：基于 role 的访问控制（RBAC 基础）

---

## 下一章

`app3/` — 将 Vue 版 JWT 改为 **OAuth2 标准**，Swagger 自动认证。

---

## 许可证

MIT License
