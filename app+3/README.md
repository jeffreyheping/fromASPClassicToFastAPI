# Todo FastAPI + Nuxt（app+3 版本）

> ✅ **已实现** — FastAPI + Nuxt 4 + SSR + BFF

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

## 项目结构

```
app+3/
├── backend/                    ← FastAPI 后端
│   ├── main.py                 # 入口（无 CORS，BFF 同源）
│   ├── config.py               # todo+3.db
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/todos.py
│
└── frontend/                   ← Nuxt 4 前端
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
    │   └── useTodos.ts         # useFetch 封装
    └── server/api/
        └── todos/[...].ts      # BFF 代理层
```

---

## 快速开始

### 环境要求

| 组件 | 版本 |
|------|------|
| Python | 3.9+ |
| Node.js | 20+ |
| npm / pnpm | 最新版 |

### 运行后端

```bash
cd app+3/backend

# 安装依赖
pip install fastapi uvicorn sqlalchemy pydantic --break-system-packages

# 启动服务（端口 8012）
uvicorn main:app --port 8012 --reload
```

### 运行前端

```bash
cd app+3/frontend

# 安装依赖
npm install

# 启动开发服务器（端口 3000）
npm run dev
```

### 访问地址

- 前端：http://localhost:3000
- 后端 API：http://localhost:8012/docs

---

## 核心实现

### 1. BFF 代理层

`server/api/todos/[...].ts` 捕获所有 `/api/todos/*` 请求，转发到 FastAPI：

```typescript
export default defineEventHandler(async (event) => {
  const backendUrl = 'http://localhost:8012'
  const path = event.path.replace('/api/', '')
  
  return $fetch(`${backendUrl}/api/${path}`, {
    method: event.method,
    body: await readBody(event)
  })
})
```

**效果**：浏览器只看到 `/api/todos`，不知道 FastAPI 的存在。同源，无 CORS 问题。

### 2. SSR 数据获取

`composables/useTodos.ts` 使用 `useFetch` 自动处理 SSR：

```typescript
export const useTodos = () => {
  // SSR 时服务端预取，CSR 时客户端请求
  const { data: todos, refresh } = useFetch('/api/todos')
  
  return { todos, refresh }
}
```

### 3. 文件路由

`pages/index.vue` 自动映射到 `/`。新建 `pages/about.vue` 就有 `/about` 路由。

### 4. Auto-import

组件和 composables 自动导入，不用写 `import`：

```vue
<script setup>
// ref、useFetch 自动可用
// TodoList、TodoForm 组件自动注册
const { todos } = useTodos()
</script>
```

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

## 教学演示

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

**演示实验：**

1. **SSR vs CSR**：在 `nuxt.config.ts` 中设置 `ssr: false`，对比首屏白屏时间
2. **文件路由**：新建 `pages/about.vue`，刷新浏览器就有 `/about` 路由
3. **BFF**：打开浏览器 Network 面板，只看到 `/api/todos`，看不到 `localhost:8012`

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

## 感悟：技术的轮回，生命的螺旋

做完整个项目，回过头看，会看到一个奇妙的圆。

```
app-2  服务器拼 HTML
  ↓
app-1  HTMX 局部刷新
  ↓
app    Vue CSR（客户端渲染）
  ↓
app+1  Vue + Vite（工程化）
  ↓
app+3  Nuxt SSR（又回到服务器拼 HTML）
```

**我们走了那么远，只为回到起点。**

但真的是回到起点吗？

---

### 同样的终点，不同的旅人

app-2 和 app+3，做的事情一模一样——服务器返回完整 HTML。但站在这两个终点上的人，看到的世界完全不同。

**app-2 的旅人**，手里只有 Jinja2 模板。他在模板里写 SQL，写业务逻辑，写 HTML。代码混在一起，像一团乱麻。每次用户点击，页面就闪烁一下——整页刷新，体验粗糙。但他不知道还有别的路，这就是他能看到的全部世界。

**app+3 的旅人**，手里有 Vue 组件、有文件路由、有 auto-import、有 BFF 层。他也在服务器上拼 HTML，但他的组件干净纯粹，业务逻辑在 FastAPI，数据获取用 `useFetch`。用户点击时，页面不再闪烁——CSR 交互丝滑流畅，SSR 首屏秒开。

同样的终点。但一个是从山脚出发的人，一个是翻过整座山回来的人。

---

### 为什么我们要走这一圈？

有人会问：既然 app+3 和 app-2 做的是同一件事，那中间这几步的意义是什么？

**CSR 的意义，不是取代 SSR，而是让我们理解"为什么需要 SSR"。**

如果没有经历过 app 的白屏等待，你不会懂 SSR 的价值。
如果没有经历过 app+1 的手动配置，你不会懂 Nuxt 文件路由的美妙。
如果没有经历过 app-6 的模板混写，你不会懂"组件只管展示"有多清爽。

**每一站，都是为了让你在下一站说一句："原来如此。"**

---

### 技术的轮回

SSR 不是新东西。PHP、JSP、ASP Classic，二十年前就在做了。

那为什么现在又火了？

因为工具链成熟了。以前 SSR 意味着：
- 前后端代码混在一起
- 模板里写业务逻辑
- 交互体验差

现在 Nuxt/Next.js 让 SSR 意味着：
- 前后端代码分离
- 组件只管展示
- CSR 交互 + SSR 首屏

**技术是一个轮回。每隔十年，老概念会用新工具重新实现一遍。**

但每一次轮回，都不是简单的重复。螺旋上升——站在更高的地方，看同样的风景，心境已完全不同。

---

### 写在最后

这个项目从 app-6 出发，一路走到 app+3。

app-6 是退化，退到 ASP Classic 的手感，让学生看到"屎山"长什么样。
app+3 是进化，进到 Nuxt SSR 的架构，让学生看到现代 Web 开发的终点。

**从最原始的服务器渲染出发，经历客户端渲染的洗礼，最终回到服务器渲染——但这一次，带着现代工具和理念。**

这不是回到原点。

这是螺旋上升。

> "我们走了一圈，不是为了回到起点，而是为了看清起点。"
>
> —— 技术的轮回，生命的螺旋

---

## 上一步 / 下一步

- **上一步**：[app+1/README.md](../app+1/README.md) — 前后端彻底分离（Vue + Vite）
- **演进路线**：[../README.md](../README.md)
