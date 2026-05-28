# app1 项目结构

## 双 UI 架构

```
外部客人 → /      → Vue.js SPA  → /api/todos (JSON)
内部员工 → /internal → HTMX 页面  → /todos    (HTML 片段)
```

## 目录分层

| 层 | 路径 | 职责 |
|---|---|---|
| 共享层 | `core/` | config, database, models, schemas, services |
| API 路由 | `routers/api/` | JSON 返回，供 Vue 调用 |
| Web 路由 | `routers/web/` | HTML 片段返回，供 HTMX 调用 |
| 模板 | `templates/` | Jinja2 (index.html=外部, internal.html=内部, partials/) |
| 静态文件 | `static/` | Vue.js app.js + CSS (两套 UI 共享样式) |

## 启动命令

```bash
cd C:\Users\jeffr\Documents\GitHub\fromASPClassicToFastAPI
"C:\Users\jeffr\anaconda3\python.exe" -m uvicorn app1.main:app --host 0.0.0.0 --port 8005 --reload
```

## 与原项目的对应关系

- `app/routers/todos.py` → `app1/routers/api/todos.py` (CRUD 逻辑抽到 services)
- `app-1/routers/todos.py` → `app1/routers/web/todos.py` (CRUD 逻辑抽到 services)
- 两个项目的 database.py/models.py 完全一样 → `app1/core/` 共享
- `app/schemas.py` → `app1/core/schemas.py`
- `app/static/js/app.js` → `app1/static/js/app.js` (不变，API 路径匹配)
- 两个 style.css 合并为 `app1/static/css/style.css`

## 注意

- 认证部分暂未实现（用户说晚点从长计议）
- `app1/` 独立于 `app/` 和 `app-1/`，原项目未改动
- Import 路径：routers 下级用 `...core` (三个点) 引用 `app1.core`
- **`--reload` 缓存坑**：修改路由代码后 `--reload` 有时不生效，需先清 `__pycache__` 目录再重启
- **端口占用**：重启前先 `netstat -ano | findstr ":8005"` 检查，有残余进程用 `taskkill /F /PID <pid>` 杀掉
