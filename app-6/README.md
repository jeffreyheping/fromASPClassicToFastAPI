# app-6 — 退无可退版

> 最原始的 Web 开发方式：模板即路由 + Mako 混写 + sqlite3 裸 SQL

---

## 项目简介

`app-6/` 是教学进化链的**退化终点**——回到 ASP/JSP/PHP 时代的开发方式：

- **模板即路由**：`templates/list.mako` 就是 `/list` 路由
- **模板混写业务逻辑**：`<% %>` 代码块里直接写 Python + SQL
- **纯 SQL 操作**：sqlite3 标准库，无 ORM
- **无 Pydantic、无 SQLAlchemy、无路由装饰器**

### 为什么用 Mako，而不是 FastAPI 默认的 Jinja2？

关键的工程技术原因：**Jinja2 刻意不支持在模板里写 Python 代码**。它的设计哲学是"模板只做展示"，代码块（`{% %}`）仅限控制流和变量操作，你不能写 `import sqlite3` 或 `conn.execute()`。

Mako 则没有这个限制——`<% %>` 里可以写任意 Python 语句。这让 app-6 的"模板即路由"风格成为可能：每个页面在自己的 `.mako` 文件里完成数据库连接、SQL 执行、结果渲染，全过程无需离开模板文件。如果换成 Jinja2，SQL 只能写到 `server.py` 的路由函数里——但那正是 app-5 要做的进化。

与 [Py4web 的 todo_classic_-2](https://github.com/jeffreyheping/fromASPClassicToPy4web/tree/main/apps/todo_classic_-2) 理念一致，但用 FastAPI + Mako 实现。

---

## 项目结构

```
app-6/
├── main.py                # 写一次不改：模板即路由核心
├── config.py              # 配置（路径常量）
├── templates/             # 所有页面都在这里
│   ├── index.mako         # / 首页（重定向）
│   ├── list.mako          # /list 待办列表
│   ├── add.mako           # /add 新增表单
│   ├── add_db.mako        # /add_db 新增处理
│   ├── edit.mako          # /edit 编辑表单
│   ├── edit_db.mako       # /edit_db 编辑处理
│   ├── delete_db.mako     # /delete_db 删除处理
│   ├── done_db.mako       # /done_db 切换状态
│   └── ...
├── static/
│   └── style.css          # 样式
└── README.md
```

**注意**：没有 `db.py`、没有 `models.py`、没有 `routers/`。
数据库文件 `todo-6.db` 存放在**根目录**。
一切业务逻辑都在 `templates/` 里，`main.py` 是黑盒，写一次不改。

---

## 核心设计

### main.py — 写一次不改

```python
# URL 直接映射到 templates/ 下的 .mako 文件
# /list     -> templates/list.mako
# /add      -> templates/add.mako
# /         -> templates/index.mako

@app.get("/{path:path}")
@app.post("/{path:path}")
async def page(request: Request, path: str = "index"):
    # 1. 找模板文件
    # 2. 渲染 Mako 模板（注入 request, redirect, DB_PATH, sqlite3）
    # 3. 返回 HTML
```

### 模板内可用的变量

| 变量 | 说明 |
|------|------|
| `request` | FastAPI Request 对象 |
| `redirect(url)` | 重定向到指定 URL |
| `DB_PATH` | 数据库文件路径 |
| `sqlite3` | sqlite3 模块 |
| `form` | POST 表单数据（字典）|
| `query` | URL 查询参数（字典）|

### Mako 语法

```mako
<%
# Python 代码块
conn = sqlite3.connect(DB_PATH)
todos = conn.execute("SELECT * FROM todo").fetchall()
conn.close()
%>

% for todo in todos:
    <p>${todo['info']}</p>  <%-- 输出变量 --%>
% endfor

% if todo['status'] == 1:
    <span>已完成</span>
% else:
    <span>待办</span>
% endif
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install fastapi uvicorn mako python-multipart --break-system-packages
```

### 2. 运行

```bash
uvicorn app-6.main:app --port 8006 --reload
```

### 3. 访问

- 首页：http://localhost:8006/ （自动重定向到 /list）
- 列表：http://localhost:8006/list
- 新增：http://localhost:8006/add

---

## 开发流程

```
1. main.py 写一次，不再改
2. 在 templates/ 下新增 .mako 文件
3. 刷新浏览器，立即生效（无需重启）
```

新增页面示例：

```bash
# 创建 templates/about.mako
cat > templates/about.mako << 'EOF'
<!DOCTYPE html>
<html>
<head><title>关于</title></head>
<body>
    <h1>关于页面</h1>
    <a href="/list">返回列表</a>
</body>
</html>
EOF

# 立即访问 http://localhost:8006/about
```

---

## SQL 对照表

| 操作 | 代码 |
|------|------|
| 查询全部 | `conn.execute("SELECT * FROM todo ORDER BY id DESC").fetchall()` |
| 查询单条 | `conn.execute("SELECT * FROM todo WHERE id = ?", (id,)).fetchone()` |
| 插入 | `conn.execute("INSERT INTO todo (info, status) VALUES (?, 0)", (info,))` |
| 更新 | `conn.execute("UPDATE todo SET info = ? WHERE id = ?", (info, id))` |
| 删除 | `conn.execute("DELETE FROM todo WHERE id = ?", (id,))` |
| 切换状态 | `conn.execute("UPDATE todo SET status = 1 - COALESCE(status, 0) WHERE id = ?", (id,))` |

---

## 与 Py4web 版的对照

| | Py4web (`todo_classic_-2`) | app-6 (FastAPI + Mako) |
|--|---------------------------|------------------------|
| 模板后缀 | `.html` | `.mako` |
| 代码块 | `[[ ]]` / `[[= ]]` | `<% %>` / `${}` |
| 路由机制 | 自动扫描 `templates/*.html` | 自动扫描 `templates/*.mako` |
| 全局变量 | `request`, `redirect`, `URL`, `sqlite3`, `DB_PATH` | `request`, `redirect`, `DB_PATH`, `sqlite3`, `form`, `query` |
| 重定向 | `redirect('/list')` | `redirect('/list')` |

---

## 教学价值

1. **感受原始开发**：没有 ORM、没有验证框架、没有类型提示
2. **模板即路由**：最直观的路由理解方式
3. **SQL 裸写**：理解 ORM 背后的真实操作
4. **main.py 写一次不改**：体会"约定优于配置"

---

## 许可证

MIT License
