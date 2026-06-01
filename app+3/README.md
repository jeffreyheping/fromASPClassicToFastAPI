# Todo FastAPI + Nuxt（app+3 版本）

> 🚧 **预告** — 本项目尚未实现，以下为设计方案

---

## 项目简介

`app+3/` 是演进链的**第 7 步**——把前端从 Vue/Vite 升级到 **Nuxt 4**，引入服务端渲染（SSR）与文件系统路由。

- **后端不变**：FastAPI 继续提供 RESTful API，和 app+1 的后端完全一致
- **前端升级**：Vue + Vite 单页应用 → Nuxt 4 全栈框架
- **关键收益**：SSR（首屏更快、SEO 友好）、文件路由（零配置）、auto-import（少写 import）

这是从"手动搭建前端工程"到"使用前端框架"的关键一步。

---

## 与 app+1 的区别

| | app+1/ | app+3/ |
|--|--------|--------|
| **前端框架** | Vue 3 + Vite | Nuxt 4（基于 Vue 3 + Vite） |
| **路由方式** | 手写 Vue Router | 文件系统路由（`pages/` 目录即路由） |
| **渲染模式** | 纯客户端渲染（CSR） | SSR / SSG / CSR 可混合 |
| **组件导入** | 手动 `import` | auto-import（Nuxt 自动扫描） |
| **首屏性能** | 白屏等待 JS 加载 | 服务端预渲染 HTML，秒开 |
| **SEO** | 搜索引擎看不到内容 | 服务端返回完整 HTML |
| **构建输出** | `dist/`（纯静态） | `.output/`（SSR 服务 + 静态资源） |
| **后端** | FastAPI（不变） | FastAPI（不变） |
| **开发运行** | `uvicorn` + `npm run dev` | `uvicorn` + `npm run dev`（方式不变） |

---

## 预计项目结构

```
app+3/
├── backend/                    ← Python 工程（从 app+1 复制，不改）
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # todo+3.db
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   └── todos.py
│   └── requirements.txt
│
└── frontend/                   ← Nuxt 4 工程
    ├── nuxt.config.ts          # Nuxt 配置（SSR、代理、模块）
    ├── package.json            # vue, nuxt, @nuxt/ui 等
    ├── app.vue                 # 根组件
    ├── pages/
    │   └── index.vue           # 首页（文件路由，无需配置）
    ├── components/
    │   ├── TodoList.vue        # 列表组件
    │   ├── TodoForm.vue        # 新增表单
    │   └── TodoItem.vue        # 单项组件
    ├── composables/
    │   └── useTodos.ts         # 数据逻辑（useFetch 封装）
    ├── server/                 # Nuxt 服务端（可选：API 代理层）
    │   └── api/
    │       └── todos.get.ts    # 服务端代理 FastAPI（隐藏后端地址）
    └── public/
        └── favicon.ico
```

> 注：以上结构为设计方案，实际实现可能调整。

---

## 核心概念预告

### 1. 什么是 SSR（服务端渲染）？

app+1 的 Vue 是**客户端渲染（CSR）**：

```
浏览器请求 → 空 HTML → 下载 JS → Vue 在浏览器里渲染 → 看到页面
                        ↑ 这段时间用户看白屏
```

Nuxt 的 SSR：

```
浏览器请求 → Nuxt 服务端执行 Vue → 返回完整 HTML → 浏览器直接显示
                                      ↑ 秒开，搜索引擎也能读到内容
```

### 2. 文件系统路由

Vue 需要手动写路由配置：

```javascript
// app+1 的做法
const routes = [
  { path: '/', component: Home },
  { path: '/about', component: About },
]
```

Nuxt 的 `pages/` 目录**就是路由**：

```
pages/
├── index.vue      → /
├── about.vue      → /about
└── todos/
    └── [id].vue   → /todos/:id（动态路由）
```

零配置，文件名即路由。

### 3. Auto-import（自动导入）

app+1 需要手动 import：

```vue
<script setup>
import { ref } from 'vue'
import { getTodos } from '../api'
</script>
```

Nuxt 的 composables 和组件**不用写 import**：

```vue
<script setup>
// ref、useFetch、useRoute 全自动可用
// components/ 下的组件自动注册
const { data: todos } = await useFetch('/api/todos')
</script>
```

### 4. Nuxt 服务端代理（可选进阶）

可以用 Nuxt 的 `server/api/` 作为**BFF 层**（Backend For Frontend）：

```
浏览器 → Nuxt (SSR + API 代理) → FastAPI
         ↑ 同源，无 CORS 问题       ↑ 只对内暴露
```

用户请求 `/api/todos`，Nuxt 收到后转发给 FastAPI `http://localhost:8012/api/todos`。前端不知道 FastAPI 的存在——这是生产环境的常见模式。

### 5. SSG（静态生成）

对于内容不常变的页面，Nuxt 可以**构建时**就生成静态 HTML：

```bash
npm run generate
```

生成纯静态文件，部署到 CDN，加载速度极快。同一个项目里 SSR 和 SSG 可以混用。

---

## 教学价值

这一步做完，学生就完整经历了：

```
纯 Web 整页刷新 → HTMX 局部刷新 → Vue CSR → Nuxt SSR
                                                 ↑
                                          现代 Web 开发的终点
```

Nuxt 是 Vue 生态的"集大成者"——它把路由、状态管理、数据获取、渲染策略都统一在约定优于配置的框架里。从 app+1 的手动搭建到 app+3 的框架加持，学生能理解"框架帮你省掉了什么"。

核心问题会自然浮现：
- 为什么 Vue/Vite 模式下首屏慢？（CSR 的代价）
- 为什么 /about 这种页面不需要 SSR？（SSG 的用武之地）
- BFF 层到底解决了什么问题？（CORS、安全、数据聚合）

---

## 预计环境要求

| 组件 | 说明 |
|------|------|
| Python 3.9+ | FastAPI 后端（从 app+1 迁移） |
| Node.js 20+ | Nuxt 4 需要 |
| npm / pnpm | 包管理 |
| Nuxt 4 | 前端框架 |
| @nuxt/ui | UI 组件库（可选） |

---

## 待定决策

以下设计决策将在实际开发时确定：

- [ ] Nuxt UI 版本（v2 传统写法 vs v3 新 API）→ 倾向于 v2，与已有教程对齐
- [ ] 是否引入 BFF 层（`server/api/`） → 先做最简单的 `useFetch` 直连 FastAPI，BFF 作为可选进阶
- [ ] SSR 策略（全站 SSR vs 混合模式）→ 列表页 SSR，表单交互 CSR
- [ ] 数据库名 → `todo+3.db`，端口 → FastAPI 8012 + Nuxt 3000

---

## 上一步 / 下一步

- **上一步**：[app+1/README.md](../app+1/README.md) — 前后端彻底分离（Vue + Vite）
- **演进路线**：[../README.md](../README.md)
