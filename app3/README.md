# Todo FastAPI — OAuth2 标准认证（app3版本）

> FastAPI 版「双 UI + OAuth2 认证」教学项目

---

## 项目简介

在 app1 的基础上加入完整的认证体系，Vue 端采用 **OAuth2 标准 JWT 认证**，HTMX 端采用 Session 认证，Swagger UI 原生支持一键登录。

| 访问方 | URL | 前端技术 | 认证方式 | 数据交互 |
|--------|-----|---------|---------|---------|
| 外部客人 | `/` | Vue.js 3 SPA | **OAuth2 JWT** (Bearer Token) | JSON API (`/api/todos`) |
| 内部员工 | `/internal` | HTMX + Jinja2 | **Session** (Cookie) | HTML 片段 (`/todos`) |

**核心特性：**
- Vue 版使用 OAuth2 标准端点 `/api/auth/token`
- Swagger UI 自动显示 🔒 图标，点击输入用户名密码即可认证
- 角色分流：guest → Vue 端，staff → HTMX 端
- 401 未登录时浏览器自动重定向到登录页

---

## 认证机制

### Vue 端：OAuth2 标准 JWT

```python
# core/security.py
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

async def get_current_user_oauth2(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    ...
```

Swagger UI 自动显示 🔒 图标，点击输入用户名密码即可——无需手动复制 token。

### HTMX 端：Session 认证

```python
# core/security.py
def get_current_user_session(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    ...
```

传统 session cookie 方案，配合 401 异常处理器做浏览器重定向。

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
uvicorn app3.main:app --host 0.0.0.0 --port 8007 --reload
```

### 3. 访问应用

| 页面 | 地址 | 说明 |
|------|------|------|
| Vue 版 | http://localhost:8007 | 外部客人入口 |
| HTMX 版 | http://localhost:8007/internal | 内部员工入口（需登录） |
| API 文档 | http://localhost:8007/docs | Swagger UI（带 OAuth2 认证） |

### 4. Swagger 一键认证

1. 打开 http://localhost:8007/docs
2. 点击右上角 **Authorize** 🔒 按钮
3. 输入用户名密码（需先注册）
4. 所有受保护接口自动携带 token

### 5. 测试认证流程

**Vue 版：**
1. 打开 http://localhost:8007
2. 注册/登录（OAuth2 Form 格式）
3. staff 自动跳转到 /internal

**HTMX 版：** 打开 http://localhost:8007/internal，注册后 staff 自动进入内部页面

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

## 前端登录代码（OAuth2 Form 格式）

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
4. **双认证体系**：JWT（API）+ Session（Web），各司其职
5. **401→302 重定向**：浏览器未登录时自动跳转登录页

---

## 演进路线

```
app1/ → 基础双 UI 架构（无认证）
  ↓
app3/ → 双 UI + OAuth2 认证（本项目）
  ↓
生产环境 → Auth0 / AWS Cognito / Keycloak（托管服务）
```

---

## 许可证

MIT License
