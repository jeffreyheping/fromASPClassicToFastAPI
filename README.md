# Todo FastAPI one_1

> FastAPI 版「从 ASP Classic 到前后端分离」进化课程 - 第6集（最终形态）

---

## 项目简介

这是一个基于 **FastAPI + Vue.js 3** 的待办事项应用，采用前后端分离架构。本项目是「从 ASP Classic 到现代 Web 开发」进化教学系列的 FastAPI 版本终点。

### 技术栈（版本已锁定）

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.115.0 |
| 数据库 | SQLite + SQLAlchemy | 2.0.36 |
| 数据验证 | Pydantic | 2.9.2 |
| 模板引擎 | Jinja2 | 3.1.2 |
| ASGI 服务器 | Uvicorn | 0.32.0 |
| 前端框架 | Vue.js 3 (Options API) | 最新版 (CDN) |
| 样式 | 原生 CSS | - |

> ⚠️ **版本锁定说明**：本项目所有 Python 依赖版本已锁定在 `requirements.txt` 中，确保长期稳定运行。请勿随意升级，以免引入 breaking changes。

---

## 前世今生

### 起源：py4web 的 6 集进化课程

2025 年，GitHub 用户 [jeffreyheping](https://github.com/jeffreyheping) 创建了 [`fromASPClassicToPy4web`](https://github.com/jeffreyheping/fromASPClassicToPy4web) 项目，用同一个 Todo 应用演示了从 ASP Classic 到现代 Python Web 开发的完整演进路径。

原项目的核心叙事是：**"先退化到 ASP Classic 的手感，再掉头进化到现代写法"**。

6 集演进路线：

```
退化线：第1集 → 第2集 → 第3集（退到头）
进化线：第1集 → 第4集 → 第5集 → 第6集（走向现代）
```

| 集数 | 技术特点 |
|------|---------|
| 第1集 | DAL + 手动路由，业务逻辑在模板中（"四不像"起点） |
| 第2集 | 自动路由扫描，丢掉手动注册 |
| 第3集 | sqlite3 原生 SQL，退化到底 |
| 第4集 | 业务逻辑收回 Python 函数 |
| 第5集 | MVC 脚手架拆分（官方 _scaffold 结构） |
| 第6集 | **前后端分离（Vue.js + RESTful API）** ← 你在这里 |

### 为什么做 FastAPI 版本

py4web 是一个优秀的教学框架，但：

1. **受众面有限** —— 相比 Flask/FastAPI，py4web 的用户基数较小
2. **生态较封闭** —— 依赖 web2py 生态，第三方包较少
3. **未来趋势** —— FastAPI 代表了现代 Python Web 开发的方向（异步、类型安全、自动文档）

因此，我们决定将这套教学课程移植到 FastAPI，让更多开发者受益。

### 从 0 到 1 的艰辛

移植过程并非一帆风顺。我们在开发中遇到了以下坑：

#### 坑 1：SQLAlchemy 2.0 的 Base 定义变了

```python
# SQLAlchemy 1.x 的写法（报错！）
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

# SQLAlchemy 2.0 的正确写法
from sqlalchemy.orm import DeclarativeBase as _DeclarativeBase
class Base(_DeclarativeBase):
    pass
```

**教训**：SQLAlchemy 2.0 的 `DeclarativeBase` 是一个类，不是工厂函数，不能实例化。

#### 坑 2：Pydantic 2.x 的 ORM 模式配置变了

```python
# Pydantic 1.x 的写法（报错！）
class TodoSchema(BaseModel):
    class Config:
        orm_mode = True

# Pydantic 2.x 的正确写法
class TodoSchema(BaseModel):
    model_config = {"from_attributes": True}
```

**教训**：Pydantic 2.x 使用 `model_config` 替代了嵌套的 `Config` 类。

#### 坑 3：Jinja2 与 Vue.js 的语法冲突

Jinja2 和 Vue.js 都使用 `{{ }}` 语法，导致模板解析冲突：

```html
<!-- 这行代码会被 Jinja2 解析，报错 'todo' is undefined -->
<span>{{ todo.info }}</span>
```

**解决方案**：使用 Jinja2 的字符串拼接输出 `{{` 和 `}}`：

```html
<!-- Jinja2 会输出 {{ todo.info }}，留给 Vue.js 处理 -->
<span>{{ '{{' }} todo.info {{ '}}' }}</span>
```

**教训**：混合使用服务端模板和前端框架时，要注意语法冲突。另一种方案是用 `{% raw %}` 包裹 Vue.js 代码块，但对于需要混合使用的情况，字符串拼接更灵活。

#### 坑 4：app.mount 的顺序至关重要

```python
# 错误的顺序（静态文件会拦截所有请求！）
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(todos.router)  # 永远不会被匹配

# 正确的顺序
app.include_router(todos.router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
```

**教训**：`app.mount` 是「前缀匹配」，一旦匹配成功就不会继续查找其他路由。必须放在所有路由之后。

---

## 项目结构

```
todo_fastapi_one_1/
├── app/
│   ├── __init__.py              # 空文件，标识 Python 包
│   ├── main.py                  # FastAPI 入口 + 路由注册（使用官方 Jinja2Templates）
│   ├── config.py                # 配置（数据库 URI）
│   ├── database.py              # SQLAlchemy 引擎 + 会话管理
│   ├── models.py                # 数据模型（Todo 表）
│   ├── schemas.py               # Pydantic 模型（请求/响应验证）
│   ├── routers/
│   │   ├── __init__.py          # 空文件
│   │   └── todos.py             # RESTful API 路由（5 个端点）
│   ├── static/
│   │   ├── css/style.css        # 样式
│   │   └── js/app.js            # Vue.js 3 前端逻辑
│   └── templates/
│       └── index.html           # 单页应用入口（Jinja2 + Vue.js 混合模板）
├── tests/                       # 测试目录（待补充）
├── requirements.txt             # 依赖清单（版本已锁定）
├── SETUP.md                     # 详细搭建指南（照做一定成功）
└── README.md                    # 本文件
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

> `--break-system-packages` 选项用于系统 Python 环境安装。如果你使用虚拟环境（venv/conda），可以省略此选项。

### 2. 运行项目

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### 3. 访问应用

- 前端界面：http://localhost:8000
- API 文档：http://localhost:8000/docs

### 详细搭建指南

如果你是初学者，或需要从零开始一步步搭建，请参考 [SETUP.md](./SETUP.md) 文件。该指南包含：
- 完整的目录创建命令
- 每个文件的详细代码
- 常见错误及解决方案
- 版本兼容性说明

---

## API 端点

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/api/todos` | 获取所有待办事项 |
| POST | `/api/todos` | 新增待办事项 |
| PUT | `/api/todos/{id}` | 更新待办内容 |
| PUT | `/api/todos/{id}/done` | 切换完成状态 |
| DELETE | `/api/todos/{id}` | 删除待办事项 |

---

## 核心设计决策

### 为什么使用官方 `Jinja2Templates`？

本项目采用 FastAPI 官方推荐的 `Jinja2Templates` 方式渲染模板，而非 `HTMLResponse` 直接读取文件。这样做的好处：

1. **静态文件 URL 自动生成**：使用 `{{ url_for('static', path='/css/style.css') }}`，即使静态文件路径变化，模板也能正确生成 URL
2. **模板继承和复用**：Jinja2 支持模板继承、宏、过滤器等高级特性
3. **符合官方最佳实践**：使用框架推荐的方式，便于团队协作和后续维护

**版本锁定是关键**：通过锁定 `jinja2==3.1.2` 和 `starlette==0.38.6` 版本，避免了 Jinja2 与 Starlette 的兼容性问题。

### 为什么 Vue.js 用 Options API 而不是 Composition API？

教学场景下，Options API 更直观：

- `data()`、`methods`、`mounted` 一目了然
- 与 py4web 原项目的 Vue 代码风格一致
- 初学者更容易理解

### 为什么数据库用 SQLite？

- 零配置，开箱即用
- 单文件，便于教学演示
- 生产环境可无缝迁移到 PostgreSQL/MySQL

---

## 从 here 到 there

本项目是 FastAPI 版进化课程的「终点图景」。如果你想完整学习这个进化过程，可以参考以下路线：

| 阶段 | 内容 | 对应 py4web 原项目 |
|------|------|-------------------|
| 第1集 | FastAPI + Jinja2 + 手动路由，逻辑在模板 | `todo_classic` |
| 第2集 | FastAPI + Jinja2 + 自动路由 | `todo_classic_-1` |
| 第3集 | FastAPI + sqlite3 原生 SQL | `todo_classic_-2` |
| 第4集 | 业务逻辑收回路由函数 | `todo_classic_1` |
| 第5集 | MVC 脚手架拆分 | `todo_classic_one` |
| 第6集 | **前后端分离（本项目）** | `todo_classic_one_1` |

---

## 经验教训总结

### 对框架设计者的启示

1. **初学者需要「终点图景」** —— py4web 的 `_scaffold` 和 `todo` 示例给出了明确的「官方推荐结构」，这对教学极其重要。FastAPI 缺乏这种「官方脚手架」，初学者容易迷失。

2. **版本兼容性要向前兼容** —— SQLAlchemy 2.0 和 Pydantic 2.x 的破坏性变更给迁移带来了巨大成本。框架升级时应提供更平滑的迁移路径。

3. **错误信息要友好** —— `TypeError: unhashable type: 'dict'` 这种错误对初学者极不友好。框架应该捕获常见错误并给出 actionable 的提示。

### 对开发者的启示

1. **版本锁定是教学项目的必需品** —— 本项目的 `requirements.txt` 锁定了所有依赖版本，确保孩子们无论何时按照步骤操作，都能得到相同的运行环境。这是教学项目与生产项目的核心差异。

2. **官方推荐 + 版本锁定 = 可靠** —— 我们最初遇到 Jinja2 兼容性问题，第一反应是用 `HTMLResponse` 绕过。但用户坚持「既然版本必须锁定，不妨用旧版本实现官方推荐的方式」。实践证明这是正确的：锁定版本后，官方 `Jinja2Templates` 工作完美。

3. **顺序很重要** —— `app.mount` 的顺序、中间件的顺序、路由的注册顺序，都可能影响应用行为。理解框架的路由匹配机制至关重要。

---

## 致谢

- [jeffreyheping](https://github.com/jeffreyheping) —— 原 py4web 进化课程作者
- [Sebastián Ramírez](https://github.com/tiangolo) —— FastAPI 作者
- [Massimo Di Pierro](https://github.com/mdipierro) —— py4web/web2py 作者

---

## 许可证

MIT License

---

> "先退化到 ASP Classic 的手感，再掉头进化到现代写法。"
> 
> —— jeffreyheping
