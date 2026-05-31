# 项目演进路线

```
app-6 → app-5 → app-2 → app-1 → app → app+1
 模板    路由    ORM    HTMX   Vue   架构分离
 即路由  分离   抽象    局部刷新 SPA
```

## 各版本速览

| 版本 | 端口 | 数据库 | 核心特征 | 启动命令 |
|------|------|--------|---------|---------|
| app-6 | 8006 | todo-6.db | Mako 模板即路由，单文件 server.py | `uvicorn app-6.server:app --host 0.0.0.0 --port 8006 --reload`（需 cd 到 app-6 目录） |
| app-5 | 8005 | todo-5.db | 路由分离 + Jinja2 + raw sqlite3 | `uvicorn app-5.main:app --host 0.0.0.0 --port 8005 --reload` |
| app-2 | 8002 | todo-2.db | 纯 Web 整页刷新 + ORM | `uvicorn app-2.main:app --host 0.0.0.0 --port 8002 --reload` |
| app-1 | 8003 | todo_htmx.db | HTMX 局部刷新 | `uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload` |
| app | 8000 | todo.db | Vue.js SPA 前后端分离 | `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload` |
| app+1 | ? | ? | 前后端彻底分离架构 | — |

## 废弃目录

- `[Abandon]app1/` — 原双 UI 合并版
- `[Abandon]app2/` — 原认证版
- `[Abandon]app3/` — 原 OAuth2 + 双 UI
- `[Abandon]app4/` — 原 OAuth2 + 测试版

## 注意事项

- Python：`C:\Users\jeffr\anaconda3\python.exe`
- 启动前先检查端口占用：`netstat -ano | findstr ":800X"`
- `--reload` 有时对 mount 顺序/结构性变更不热重载，需要手动重启
