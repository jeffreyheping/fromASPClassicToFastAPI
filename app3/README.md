# Todo FastAPI — OAuth2 标准认证（app3版本）

> FastAPI 版「OAuth2 标准认证」教学项目 - 从手写 JWT 到行业标准

---

## 项目简介

`app3/` 是 `app2/` 的进化版本，将 Vue 版的**自定义 JWT 认证**改为 **OAuth2 标准认证**，Swagger UI 原生支持一键登录。

| 访问方 | URL | 前端技术 | 认证方式 | 数据交互 |
|--------|-----|---------|---------|---------|
| 外部客人 | `/` | Vue.js 3 SPA | **OAuth2 JWT** (Bearer Token) | JSON API (`/api/todos`) |
| 内部员工 | `/internal` | HTMX + Jinja2 | **Session** (Cookie) | HTML 片段 (`/todos`) |

**核心改进：**
- Vue 版登录端点改为 `/api/auth/token`（OAuth2 标准）
- Swagger UI 自动显示锁图标，点击输入用户名密码即可认证
- 与 Auth0、AWS Cognito 等托管服务概念一致

---

## 与 app2 的区别

| 项目 | 数据库 | Vue 版认证 | Swagger 支持 |
|------|--------|-----------|-------------|
| `app2/` | `todo2.db` | 自定义 JWT | ❌ 手动输入 token |
| `app3/` | `todo3.db` | **OAuth2 标准** | ✅ 一键登录 |

**代码改动：**
- `core/security.py`: `HTTPBearer` → `OAuth2PasswordBearer`
- `routers/api/auth.py`: `/login` → `/token` (Form 格式)
- `routers/api/todos.py`: `get_current_user_jwt` → `get_current_user_oauth2`
- `static/js/app.js`: JSON 登录 → Form 格式登录

---

## 认证机制对比

### app2 自定义 JWT

```python
# 自定义依赖
_bearer_scheme = HTTPBearer()

def get_current_user_jwt(credentials: HTTPAuthorizationCredentials = Depends(_bearer_scheme)):
    payload = decode_access_token(credentials.credentials)
    ...
```

**Swagger：** 需手动复制 token 到输入框

### app3 OAuth2 标准

```python
# FastAPI 原生
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user_oauth2(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    ...
```

**Swagger：** 自动显示 🔒 图标，点击输入用户名密码即可

---

## 技术栈

| 层级 | 技术 | 版本 | 用途 |
|------|------|------|------|
| 后端框架 | FastAPI | 0.115.0 | Web 框架 |
| 认证标准 | OAuth2 + JWT | - | 行业标准认证 |
| 数据库 | SQLite + SQLAlchemy | 2.0.36 | 数据持久化 |
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
uvicorn app3.main:app --host 0.0.0.0 --port 8008 --reload
```

### 3. 访问应用

| 页面 | 地址 | 说明 |
|------|------|------|
| Vue 版 | http://localhost:8008 | 外部客人入口 |
| HTMX 版 | http://localhost:8008/internal | 内部员工入口（需登录） |
| API 文档 | http://localhost:8008/docs | Swagger UI（带 OAuth2 认证） |

### 4. Swagger 一键认证

1. 打开 http://localhost:8008/docs
2. 点击右上角 **Authorize** 🔒 按钮
3. 输入用户名密码（需先注册）
4. 所有受保护接口自动携带 token

### 5. 测试认证流程

**Vue 版：**
1. 打开 http://localhost:8008
2. 注册/登录（OAuth2 Form 格式）
3. staff 自动跳转到 /internal

**HTMX 版：** 与 app2 相同

---

## 项目结构

```
app3/
├── main.py                     # 入口
├── core/
│   ├── config.py               # 数据库配置（todo3.db）
│   ├── security.py             # OAuth2 + Session 认证工具
│   ├── models.py               # User + Todo 模型
│   └── services.py             # 业务逻辑
├── routers/
│   ├── api/                    # Vue 版 API 路由
│   │   ├── auth.py             # OAuth2 登录/注册
│   │   └── todos.py            # Todo CRUD（需 OAuth2）
│   └── web/                    # HTMX 版 Web 路由
│       ├── auth.py             # Session 登录/注册
│       └── todos.py            # Todo CRUD（需 Session）
├── templates/                  # Jinja2 模板
├── static/                     # CSS/JS
└── README.md
```

---

## 核心代码对比：app2 vs app3

### 登录端点

| | app2 | app3 |
|--|------|------|
| **URL** | `/api/auth/login` | `/api/auth/token` |
| **方法** | POST JSON | POST Form |
| **参数** | `{"username": "x", "password": "y"}` | `username=x&password=y` |
| **返回** | `{access_token, user}` | `{access_token, token_type}` |

### 前端登录代码

**app2 (JSON)：**
```javascript
const res = await fetch(`${AUTH_API}/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({username, password}),
});
```

**app3 (OAuth2 Form)：**
```javascript
const formData = new URLSearchParams();
formData.append('username', username);
formData.append('password', password);

const res = await fetch(`${AUTH_API}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: formData,
});
```

---

## 学习要点

1. **OAuth2 密码模式**：标准流程、Form 格式、Bearer Token
2. **FastAPI 集成**：`OAuth2PasswordBearer` + `Depends`
3. **Swagger 自动认证**：一键登录，自动携带 token
4. **标准的好处**：与 Auth0、AWS Cognito 概念互通

---

## 演进路线

```
app1/ → 基础双 UI 架构
  ↓
app2/ → 手写 JWT + Session（理解原理）
  ↓
app3/ → OAuth2 标准（行业实践）
  ↓
生产环境 → Auth0 / AWS Cognito / Keycloak（托管服务）
```

---

## 许可证

MIT License
