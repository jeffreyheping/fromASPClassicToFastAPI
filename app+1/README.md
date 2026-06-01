# Todo FastAPI — 前后端彻底分离（app+1版本）

> 从 `app/` 向前一步：Vue 前端从 FastAPI 模板中剥离，成为独立的 Node.js 工程

---

## 项目简介

`app+1/` 演示**前后端彻底分离**的架构：

- **后端**：FastAPI 只提供 API，不渲染 HTML
- **前端**：独立的 Vue + Vite 工程，通过 `npm` 管理依赖
- **通信**：前端通过 HTTP 请求调用后端 API
- **开发**：两个独立进程，两个端口

这是从"模板渲染"到"前后端分离"的关键一步。

---

## 与 app/ 的区别

| | app/ | app+1/ |
|--|------|--------|
| **前端位置** | 嵌在 FastAPI 模板里 | 独立 Node.js 工程 |
| **构建工具** | 无（CDN 引入 Vue） | Vite |
| **包管理** | 无 | npm |
| **开发运行** | `uvicorn` 一个进程 | `uvicorn` + `npm run dev` 两个进程 |
| **前端端口** | 同后端（8005） | 5173（Vite 默认） |
| **API 调用** | 同源 `/api/todos` | 通过 Vite 代理转发 |
| **部署方式** | 后端渲染 | 前端静态文件 + 后端 API |

---

## 项目结构

```
app+1/
├── backend/                    ← Python 工程（FastAPI 纯 API）
│   ├── main.py                 # 入口，配置 CORS
│   ├── config.py               # 数据库配置（todo+1.db）
│   ├── database.py             # 数据库连接
│   ├── models.py               # Todo 模型
│   ├── schemas.py              # 数据验证
│   ├── routers/
│   │   └── todos.py            # /api/todos CRUD
│   └── requirements.txt        # Python 依赖
│
└── frontend/                   ← Node.js 工程（Vue + Vite）
    ├── package.json            # npm 依赖配置
    ├── vite.config.js          # Vite 配置（API 代理）
    ├── index.html              # HTML 入口
    └── src/
        ├── main.js             # Vue 应用入口
        ├── App.vue             # 根组件（从 app.js 迁移）
        ├── api.js              # API 调用封装
        └── style.css           # 样式
```

---

## 环境准备

### 1. 后端环境（Python）

```bash
# 进入后端目录
cd backend

# 安装依赖
pip install fastapi uvicorn sqlalchemy pydantic --break-system-packages
```

### 2. 前端环境（Node.js）

```bash
# 进入前端目录
cd frontend

# 安装依赖（只需要执行一次）
npm install
```

**什么是 `npm install`？**

`npm` 是 Node.js 的包管理工具，类似 Python 的 `pip`。

- `package.json` 里列出了项目需要的依赖（如 Vue、Vite）
- `npm install` 会自动下载这些依赖到 `node_modules/` 目录
- 下载完成后，就可以运行项目了

**常见报错：**

```
npm: command not found
```

**解决：** 安装 Node.js
- 官网下载：https://nodejs.org/
- 或命令行安装：`sudo apt install nodejs npm`

---

## 运行项目

需要**两个终端窗口**同时运行：

### 终端 1：启动后端

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8010 --reload
```

- 后端地址：http://localhost:8010
- API 文档：http://localhost:8010/docs

### 终端 2：启动前端

```bash
cd frontend
npm run dev
```

- 前端地址：http://localhost:5173
- Vite 会自动打开浏览器（或手动访问）

---

## 核心概念讲解

### 1. 为什么需要两个进程？

前后端分离后，前端和后端是**两个独立的应用**：

- **后端**：只关心数据（数据库操作、API 接口）
- **前端**：只关心展示（界面、交互）

它们通过 HTTP 协议通信，就像两个独立的服务器。

### 2. 什么是 Vite？

Vite 是 Vue 官方推荐的**构建工具**，类似 Python 的 `uvicorn`：

- **开发时**：提供热更新（改代码自动刷新浏览器）
- **构建时**：把 Vue 代码打包成静态文件（HTML/CSS/JS）
- **代理功能**：把 `/api` 请求转发到后端，避免跨域问题

### 3. 跨域问题（CORS）

浏览器安全策略：**前端页面不能随意访问其他域名的 API**。

- 前端运行在 `http://localhost:5173`
- 后端运行在 `http://localhost:8010`
- 端口不同 = 域名不同 = 跨域

**解决方案：**

1. **开发时**：Vite 代理（前端请求 `/api`，Vite 转发到后端）
2. **生产时**：后端配置 CORS（允许前端域名访问）

### 4. API 调用封装（api.js）

```javascript
// 前端代码不再直接写 fetch，而是调用封装好的函数
import { getTodos, createTodo } from './api.js'

// 使用时像调用本地函数一样简单
const todos = await getTodos()
```

好处：
- 统一处理错误
- 统一配置 API 地址
- 代码更清晰

---

## 部署方式

### 开发环境（当前）

```
浏览器 → 前端开发服务器(5173) → Vite代理 → 后端(8010)
```

### 生产环境

```
浏览器 → Nginx/静态托管 → 后端API
         ↓
    前端静态文件（npm run build 生成）
```

**构建命令：**

```bash
cd frontend
npm run build
```

生成 `dist/` 目录，里面是纯静态文件，可以部署到任何 Web 服务器。

---

## 学习要点

1. **npm 包管理**：理解 `package.json`、`node_modules`、`npm install`
2. **Vite 开发服务器**：热更新、代理配置
3. **跨域与 CORS**：为什么需要、如何解决
4. **API 封装**：前端如何组织 HTTP 请求
5. **前后端分离的本质**：两个独立应用通过 HTTP 通信

---

## 下一章

[app+3/](../app+3/README.md) — 引入 **Nuxt 4**，服务端渲染（SSR）与文件系统路由。

---

## 许可证

MIT License
