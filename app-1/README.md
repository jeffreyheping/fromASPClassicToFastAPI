# Todo FastAPI + HTMX

> FastAPI 版「从 ASP Classic 到前后端分离」进化课程 - 前端退化版

---

## 项目简介

这是一个基于 **FastAPI + HTMX** 的待办事项应用。与 Vue.js 版本不同，这个版本**不使用 JavaScript 框架**，而是通过 HTMX 的 HTML 属性实现局部刷新。

### 为什么做这个版本

孩子们对 Vue.js 的学习有抵触心理——JS 毕竟是新语言新天地。用 HTMX 作为过渡，让他们先更容易明白「局部刷新」这种底层原理。

### HTMX 核心理念

```html
<!-- 普通链接 - 整页刷新 -->
<a href="/todos">查看待办</a>

<!-- HTMX 链接 - 局部刷新 -->
<button hx-get="/todos" hx-target="#list" hx-swap="innerHTML">
  查看待办
</button>
```

HTMX 让 HTML 元素具备 AJAX 能力，无需编写 JavaScript 代码。

---

## 技术栈（版本已锁定）

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.115.0 |
| 数据库 | SQLite + SQLAlchemy | 2.0.36 |
| 模板引擎 | Jinja2 | 3.1.2 |
| 前端增强 | HTMX | 1.9.10 (CDN) |
| 样式 | 原生 CSS | - |

---

## 与 Vue 版本的对比

| 特性 | Vue 版本 (app/) | HTMX 版本 (app-1/) |
|------|----------------|-------------------|
| **前端技术** | Vue.js 3 + Options API | HTMX (无 JS 框架) |
| **渲染方式** | 客户端渲染 (CSR) | 服务端渲染 (SSR) + 局部刷新 |
| **数据交互** | RESTful API + JSON | 表单提交 + HTML 片段 |
| **代码位置** | `app.js` 前端逻辑 | `routers/todos.py` 后端逻辑 |
| **学习曲线** | 需学习 Vue 概念 | 只需理解 HTML 属性 |
| **适用场景** | 复杂交互应用 | 简单 CRUD、教学过渡 |

---

## 项目结构

```
app-1/
├── __init__.py
├── config.py              # 数据库配置
├── database.py            # SQLAlchemy 引擎
├── models.py              # 数据模型
├── main.py                # FastAPI 入口
├── routers/
│   ├── __init__.py        # 空文件
│   └── todos.py           # HTMX 路由（6 个端点）
├── static/
│   └── css/style.css      # 样式
├── templates/
│   ├── index.html         # 主页面
│   └── partials/
│       ├── todo_list.html # 待办列表片段
│       └── edit_form.html # 编辑表单片段
├── README.md              # 本文件
└── SETUP.md               # 详细搭建指南
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r ../requirements.txt --break-system-packages
```

### 2. 运行项目

```bash
uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload
```

### 3. 访问应用

打开浏览器访问：http://localhost:8003

---

## HTMX 核心属性详解

### `hx-post` / `hx-put` / `hx-delete`
指定请求方法和 URL：
```html
<form hx-post="/todos">...</form>
<button hx-put="/todos/1/toggle">完成</button>
<button hx-delete="/todos/1">删除</button>
```

### `hx-target`
指定更新哪个元素：
```html
<!-- 更新 id="list" 的元素 -->
<button hx-get="/todos" hx-target="#list">刷新</button>

<!-- 更新最近的 li 元素 -->
<button hx-get="/edit" hx-target="closest li">编辑</button>
```

### `hx-swap`
指定如何替换内容：
- `innerHTML` - 替换内部内容（默认）
- `outerHTML` - 替换整个元素
- `beforeend` - 在末尾追加
- `delete` - 删除元素

### `hx-confirm`
操作前确认：
```html
<button hx-delete="/todos/1" hx-confirm="确定删除吗？">删除</button>
```

### `hx-on`
事件处理：
```html
<form hx-post="/todos" hx-on::after-request="this.reset()">
```

---

## 路由端点

| 方法 | 端点 | 功能 |
|------|------|------|
| GET | `/` | 首页（完整页面） |
| GET | `/todos/list` | 获取列表片段 |
| POST | `/todos` | 新增待办 |
| GET | `/todos/{id}/edit` | 获取编辑表单 |
| PUT | `/todos/{id}` | 更新内容 |
| PUT | `/todos/{id}/toggle` | 切换完成状态 |
| DELETE | `/todos/{id}` | 删除待办 |

---

## 教学价值

### 孩子们能学到什么

1. **AJAX 的本质**：不是魔法，就是普通的 HTTP 请求
2. **局部刷新的原理**：后端返回 HTML，替换页面的一部分
3. **渐进增强**：从普通表单 → HTMX → Vue.js 的演进路径
4. **服务端渲染的优势**：首屏快、SEO 友好、代码简单

### 与 Vue 版本的学习路径

```
阶段1: HTMX 版本
   ↓ 理解「局部刷新」原理
阶段2: Vue 版本
   ↓ 理解「数据驱动」和「组件化」
阶段3: 前后端完全分离
   ↓ 理解「微服务」和「API 设计」
```

---

## 从 here  to there

完成本版本学习后，可以：

1. **对比 Vue 版本**：同样的功能，不同的实现方式
2. **添加新功能**：尝试用 HTMX 实现搜索、分页
3. **理解极限**：当交互复杂时，为什么需要 Vue/React

---

## 致谢

- [HTMX 官方文档](https://htmx.org/) - 极简的交互设计哲学
- [FastAPI](https://fastapi.tiangolo.com/) - 现代 Python Web 框架

---

## 许可证

MIT License
