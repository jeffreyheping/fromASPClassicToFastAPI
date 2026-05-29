# Todo FastAPI — 纯 Web 版（app-2版本）

> FastAPI 版「纯服务端渲染」教学项目

---

## 项目简介

完全没有任何前端框架。每一个操作都是传统的 HTTP 请求 → 服务器处理 → 整页刷新。这就是 ASP Classic / PHP 时代最原始的 Web 交互方式。

| 对比 | app-2 (纯 Web) | app-1 (HTMX) |
|------|---------------|-------------|
| 新增待办 | 提交表单 → 整页刷新 | 提交表单 → 局部替换列表 |
| 编辑待办 | 跳转编辑页 → 保存 → 跳回列表 | 就地变成编辑框 → 保存 → 就地变回列表 |
| 切换状态 | 点击链接 → 整页刷新 | 点击文字 → 局部替换列表 |
| 删除待办 | 点击链接 → confirm → 整页刷新 | 点击按钮 → confirm → 局部替换列表 |
| JS 框架 | 无 | HTMX |
| 页面闪烁 | 每次操作都闪 | 无闪烁 |

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r ../requirements.txt --break-system-packages
```

### 2. 运行项目

```bash
uvicorn app-2.main:app --host 0.0.0.0 --port 8002 --reload
```

### 3. 访问应用

| 页面 | 地址 |
|------|------|
| 首页 | http://localhost:8002 |
| API 文档 | http://localhost:8002/docs |

---

## 项目结构

```
app-2/
├── main.py                     # 入口
├── config.py                   # 数据库配置（todo-2.db）
├── database.py                 # SQLAlchemy 引擎 + 会话管理
├── models.py                   # Todo ORM 模型
├── routers/
│   └── todos.py                # 6 个路由端点（纯 Web）
├── templates/
│   ├── index.html              # 首页（列表 + 新增表单）
│   └── edit.html               # 编辑页（独立页面）
├── static/
│   └── css/style.css           # 样式
└── README.md
```

---

## 路由一览

| 方法 | 端点 | 功能 | 响应 |
|------|------|------|------|
| GET | `/` | 首页（列表 + 新增表单） | 完整 HTML 页面 |
| POST | `/todos` | 新增待办 | 303 重定向到 `/` |
| GET | `/todos/{id}/edit` | 编辑表单 | 完整 HTML 页面 |
| POST | `/todos/{id}` | 更新待办 | 303 重定向到 `/` |
| GET | `/todos/{id}/toggle` | 切换完成状态 | 303 重定向到 `/` |
| GET | `/todos/{id}/delete` | 删除待办 | 303 重定向到 `/` |

---

## 演进路线

```
app-2/ → 纯 Web，整页刷新，最接近 ASP Classic 体验
  ↓
app-1/ → 加入 HTMX，局部刷新，不写 JS 但体验飞升
  ↓
app/   → Vue.js SPA，完全前后端分离
```

---

## 许可证

MIT License
