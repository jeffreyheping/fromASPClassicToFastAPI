# Todo FastAPI + Nuxt（app+3 版本）

> ✅ **已实现** — FastAPI + Nuxt 3 + SSR + BFF

---

## 项目简介

`app+3/` 是演进链的**第 7 步**——把前端从 Vue/Vite 升级到 **Nuxt 3**，引入：
- **SSR**（服务端渲染，首屏秒开、SEO 友好）
- **BFF**（Backend For Frontend，同源无 CORS、数据聚合）
- **文件路由**（零配置，pages/ 目录即路由）
- **Auto-import**（少写 import）

**后端不变**：FastAPI 提供 RESTful API，和 app+1 完全一致。

---

## 架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                          浏览器                                      │
│  地址栏: localhost:3000  /  Network: 只有 /api/*                    │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTP
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Nuxt 3 前端 (端口 3000)                          │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────────┐    │
│  │ server/api/[...].ts — BFF 代理层                            │    │
│  │   • 拦截所有 /api/* 请求                                      │    │
│  │   • 转发到 FastAPI                                            │    │
│  │   • 返回 JSON 给前端                                          │    │
│  └─────────────────────────────────────────────────────────────┘    │
│                                                                      │
│  pages/ — 文件路由                                                  │
│  components/ — 组件（自动注册）                                      │
│  composables/ — 逻辑复用（自动导入）                                  │
│                                                                      │
│  SSR: 首屏请求时，服务端执行 Vue → 返回完整 HTML                      │
│  CSR: 后续交互，客户端增量更新                                        │
└────────────────────────┬────────────────────────────────────────────┘
                         │
                         │ HTTP (内部)
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  FastAPI 后端 (端口 8012)                            │
│                                                                      │
│  /api/todos        GET    — 获取列表                                 │
│  /api/todos        POST   — 新增                                     │
│  /api/todos/{id}   GET    — 获取单个                                 │
│  /api/todos/{id}   PUT    — 更新                                     │
│  /api/todos/{id}/done PUT — 切换完成                                 │
│  /api/todos/{id}   DELETE — 删除                                     │
│                                                                      │
│  SQLite 数据库 (todo+3.db)                                          │
└─────────────────────────────────────────────────────────────────────┘
```

**关键点**：
- 浏览器**不知道** FastAPI 的存在，只看到 `/api/*`
- Nuxt 是**同源**，无 CORS 问题
- FastAPI 只对**内网暴露**，安全

---

## 与 app+1 的区别

| | app+1/ | app+3/ |
|--|--------|--------|
| **前端框架** | Vue 3 + Vite | Nuxt 3（基于 Vue 3） |
| **渲染模式** | 纯客户端渲染（CSR） | SSR + CSR 混合 |
| **首屏性能** | 白屏等待 JS | 服务端预渲染，秒开 |
| **SEO** | 搜索引擎看不到内容 | 完整 HTML |
| **BFF** | 无，跨域需配置 CORS | ✅ 有，同源自代理 |
| **路由** | 手写 Vue Router | 文件系统路由（pages/） |
| **组件导入** | 手动 import | auto-import |
| **后端** | FastAPI | FastAPI（不变） |

---

## 项目结构

```
app+3/
├── backend/                    ← FastAPI 后端（一行不改）
│   ├── main.py
│   ├── config.py               # todo+3.db
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/todos.py
│
└── frontend/                   ← Nuxt 3 前端
    ├── nuxt.config.ts          # SSR + BFF 配置
    ├── package.json
    ├── app.vue                 # 根组件
    ├── pages/
    │   └── index.vue           # 首页（文件路由）
    ├── components/
    │   ├── TodoList.vue
    │   ├── TodoForm.vue
    │   └── TodoItem.vue
    ├── composables/
    │   └── useTodos.ts         # 数据逻辑
    └── server/api/
        └── [...].ts            # ⭐ BFF 代理层
```

---

## 快速开始

### 环境要求

| 组件 | 版本 |
|------|------|
| Python | 3.9+ |
| Node.js | 18+ |
| npm / pnpm | 最新版 |

### 启动服务

```bash
# 终端 1：后端（端口 8012）
cd app+3/backend
pip install fastapi uvicorn sqlalchemy pydantic --break-system-packages
uvicorn main:app --port 8012 --reload

# 终端 2：前端（端口 3000）
cd app+3/frontend
npm install
npm run dev
```

### 访问

- 前端：http://localhost:3000
- 后端 API：http://localhost:8012/docs

---

## 核心实现

### 1. BFF 代理层（已实现 ✅）

`server/api/[...].ts` 是 **BFF 层**，不是"可选进阶"：

```typescript
/**
 * BFF 代理层 - 代理所有 /api/* 请求到 FastAPI 后端
 * 
 * 浏览器 → Nuxt (/api/todos) → FastAPI (localhost:8012/api/todos)
 */
export default defineEventHandler(async (event) => {
  const backendUrl = useRuntimeConfig().backendUrl || 'http://localhost:8012'
  const path = event.path
  const method = event.method
  
  let body = null
  if (method !== 'GET' && method !== 'HEAD') {
    body = await readBody(event)
  }
  
  // 转发到后端
  const response = await $fetch(`${backendUrl}${path}`, {
    method,
    body,
    headers: { 'Content-Type': 'application/json' }
  })
  return response
})
```

**效果**：
- 浏览器 Network 面板只看到 `/api/todos`，看不到 `localhost:8012`
- 同源，无 CORS 问题
- FastAPI 只在内网访问

### 2. SSR 数据获取

`composables/useTodos.ts` 使用 `useFetch`，自动处理 SSR：

```typescript
export const useTodos = () => {
  // SSR 时：服务端预取 → 首次访问就有数据
  // CSR 时：客户端请求 → 后续增量更新
  const { data: todos, refresh } = useFetch<Todo[]>('/api/todos')
  
  const addTodo = async (info: string) => {
    await $fetch('/api/todos', { method: 'POST', body: { info } })
    await refresh()
  }
  
  return { todos, refresh, addTodo, updateTodo, toggleDone, deleteTodo }
}
```

### 3. 文件路由

`pages/` 目录就是路由，零配置：

```
pages/
├── index.vue      → /
├── about.vue      → /about
└── todos/
    └── [id].vue   → /todos/:id
```

### 4. Auto-import

组件和 composables 自动导入：

```vue
<script setup>
// ref、useFetch、useRoute 自动可用
// TodoList、TodoForm 组件自动注册
const { todos, addTodo } = useTodos()
</script>
```

---

## 教学演示

学生经历了完整演进：

```
app-2  服务器拼 HTML（原始）
  ↓
app-1  HTMX 局部刷新
  ↓
app    Vue CSR（客户端渲染）
  ↓
app+1  Vue + Vite（工程化）
  ↓
app+3  Nuxt SSR + BFF（现代全栈）
```

**核心演示**：

1. **SSR vs CSR**：在 `nuxt.config.ts` 设置 `ssr: false`，对比首屏
2. **文件路由**：新建 `pages/about.vue`，自动有路由
3. **BFF**：打开 Network 面板，只有 `/api/*`，没有 `localhost:8012`

---

## 上一步 / 下一步

- **上一步**：[app+1/README.md](../app+1/README.md) — 前后端分离（Vue + Vite）
- **演进路线**：[../README.md](../README.md)
