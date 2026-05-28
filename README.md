# From ASP Classic to FastAPI

> FastAPI 版「从 ASP Classic 到现代 Web 开发」进化课程

---

## 项目简介

本项目是 [fromASPClassicToPy4web](https://github.com/jeffreyheping/fromASPClassicToPy4web) 的 FastAPI 移植版本，用同一个 Todo 应用演示从传统 Web 开发到现代前后端分离的完整演进路径。

**核心理念**：先退化到 ASP Classic 的手感，再掉头进化到现代写法。

---

## 项目结构

```
todo_fastapi_one_1/
├── app/                    # Vue.js 版本 - 前后端分离
│   ├── main.py             # FastAPI + RESTful API
│   ├── static/js/app.js    # Vue.js 3 前端
│   ├── templates/          # Jinja2 模板
│   ├── README.md           # Vue 版本说明
│   └── SETUP.md            # Vue 版本搭建指南
├── app-1/                  # HTMX 版本 - 前端退化版
│   ├── main.py             # FastAPI + HTMX
│   ├── templates/          # Jinja2 模板（含 HTMX 属性）
│   ├── README.md           # HTMX 版本说明
│   └── SETUP.md            # HTMX 版本搭建指南
├── requirements.txt        # 锁定版本的依赖清单
└── README.md               # 本文件
```

---

## 两个版本对比

| 特性 | app/ (Vue.js) | app-1/ (HTMX) |
|------|---------------|---------------|
| **架构** | 前后端分离 | 服务端渲染 + 局部刷新 |
| **前端技术** | Vue.js 3 + Options API | HTMX (无 JS 框架) |
| **数据格式** | JSON API | HTML 片段 |
| **学习曲线** | 需学习 Vue 概念 | 只需 HTML 属性 |
| **适用场景** | 复杂交互应用 | 教学过渡、简单 CRUD |
| **运行端口** | 8000 | 8003 |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt --break-system-packages
```

### 2. 运行 Vue 版本

```bash
uvicorn app.main:app --port 8000
```

访问：http://localhost:8000

### 3. 运行 HTMX 版本

```bash
uvicorn app-1.main:app --port 8003
```

访问：http://localhost:8003

---

## 技术栈（版本已锁定）

| 组件 | 版本 | 说明 |
|------|------|------|
| FastAPI | 0.115.0 | Web 框架 |
| Uvicorn | 0.32.0 | ASGI 服务器 |
| SQLAlchemy | 2.0.36 | ORM |
| Pydantic | 2.9.2 | 数据验证 |
| Jinja2 | 3.1.2 | 模板引擎 |
| Starlette | 0.38.6 | ASGI 工具集 |

---

## 教学价值

### 学习路径

```
阶段 1: HTMX 版本 (app-1/)
   ↓ 理解「局部刷新」的底层原理
阶段 2: Vue.js 版本 (app/)
   ↓ 理解「数据驱动」和「组件化」
阶段 3: 前后端完全分离
   ↓ 理解「微服务」和「API 设计」
```

### 关键对比点

1. **同样的功能，不同的实现**
   - 新增待办：Vue 用 `fetch` + JSON，HTMX 用 `hx-post` + HTML
   - 列表渲染：Vue 用 `v-for`，HTMX 用 Jinja2 `{% for %}`
   - 状态切换：Vue 用 `toggleDone()` 方法，HTMX 用 `hx-put` 属性

2. **渐进式学习**
   - 先通过 HTMX 理解 AJAX 本质（就是 HTTP 请求）
   - 再通过 Vue 理解现代前端框架的优势
   - 最后理解什么时候该用什么技术

3. **版本锁定的重要性**
   - 所有依赖版本锁定在 `requirements.txt`
   - 确保教学环境长期稳定
   - 避免「在我机器上能跑」的问题

---

## 详细文档

| 版本 | 说明文档 | 搭建指南 |
|------|---------|---------|
| Vue.js | [app/README.md](app/README.md) | [app/SETUP.md](app/SETUP.md) |
| HTMX | [app-1/README.md](app-1/README.md) | [app-1/SETUP.md](app-1/SETUP.md) |

---

## 致谢

- [jeffreyheping](https://github.com/jeffreyheping) - 原 py4web 进化课程作者
- [Sebastián Ramírez](https://github.com/tiangolo) - FastAPI 作者
- [HTMX](https://htmx.org/) - 极简的交互设计哲学

---

## 许可证

MIT License

---

> "先退化到 ASP Classic 的手感，再掉头进化到现代写法。"
>
> —— jeffreyheping
