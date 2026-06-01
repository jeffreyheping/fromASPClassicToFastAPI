# Todo FastAPI — OAuth2 标准认证 + 测试（app4版本）

> FastAPI 版「双 UI + OAuth2 认证 + pytest 测试」教学项目

---

## 项目简介

在 app3 的基础上增加了完整的自动化测试体系。为了支持测试，对配置层做了环境变量支持，main.py 改为工厂函数模式。

| 访问方 | URL | 前端技术 | 认证方式 | 数据交互 |
|--------|-----|---------|---------|---------|
| 外部客人 | `/` | Vue.js 3 SPA | **OAuth2 JWT** (Bearer Token) | JSON API (`/api/todos`) |
| 内部员工 | `/internal` | HTMX + Jinja2 | **Session** (Cookie) | HTML 片段 (`/todos`) |

**相比 app3 的核心变化：**
- `config.py` 支持环境变量覆盖（`APP4_DATABASE_URL`、`APP4_SECRET_KEY`）
- `main.py` 改为 `create_app()` 工厂函数，测试可独立创建 app 实例
- `security.py` 从 config 读取密钥，不再硬编码
- 23 个 pytest 测试覆盖 services 层和 API 层

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
uvicorn app4.main:app --host 0.0.0.0 --port 8008 --reload
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

**HTMX 版：** 打开 http://localhost:8008/internal，注册后 staff 自动进入内部页面

### 6. 运行测试

```bash
pytest app4/tests/ -v
```

测试覆盖：
- **services 层**（9 项）：CRUD 纯业务逻辑
- **认证 API**（6 项）：注册、登录、密码验证
- **Todo API**（8 项）：鉴权拦截 + CRUD 全流程

---

## 项目结构

```
app4/
├── main.py                     # 入口
├── core/
│   ├── config.py               # 数据库配置（todo4.db）
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
├── tests/                      # pytest 测试
│   ├── conftest.py              # 测试 fixtures（in-memory DB）
│   ├── test_services.py         # 业务逻辑层测试
│   ├── test_api_auth.py         # 认证 API 测试
│   └── test_api_todos.py        # Todo API 测试
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
6. **pytest 测试**：TestClient + in-memory SQLite + dependency_overrides
7. **工厂函数模式**：`create_app()` 让测试独立创建 app 实例

---

## 演进路线

```
app1/ → 基础双 UI 架构（无认证）
  ↓
app3/ → 双 UI + OAuth2 认证
  ↓
app4/ → 双 UI + OAuth2 认证 + 测试（本项目）
```

---

## 许可证

MIT License
