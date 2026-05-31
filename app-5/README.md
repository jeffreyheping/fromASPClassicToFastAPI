# app-5 — 路由分离版

> 把 SQL 从模板里救出来，模板终于像模板了。

---

## 项目简介

`app-5/` 是教学进化链的第 2 步，做了一件简单的事：**把散落在 9 个 Mako 模板里的 SQL 抽到 `routers/todos.py` 的 6 个端点里**。

核心变化只有一条：模板不再写代码，只负责 `<ul>` `<li>`。业务逻辑回到路由层。

| | app-6（退无可退） | app-5（本版） | app-2（下一步） |
|---|---|---|---|
| 模板引擎 | Mako（`<% %>` 写 Python） | Jinja2（`{% %}` 只渲染） | Jinja2 |
| SQL 在哪 | 散落在 9 个 .mako 文件里 | 集中在 `routers/todos.py` | `routers/todos.py`（ORM） |
| 路由机制 | URL 映射文件名 | 装饰器显式声明 | 装饰器显式声明 |
| 文件结构 | 1 个 `server.py` | `main.py` + `database.py` + `routers/` | 同结构 |
| 数据库 | raw sqlite3 | raw sqlite3（不变） | SQLAlchemy ORM |
| 模板数 | 9 个 .mako | 2 个 .html | 2 个 .html（完全一致） |

---

## 教学价值

**这一跳只教一件事：关注点分离（Separation of Concerns）。**

app-6 把路由、SQL、HTML 全塞在同一个 `server.py` 和模板里。能跑，但改一个 SQL 要在 9 个文件里找。
app-5 把 SQL 全部抽到 6 个路由端点里，模板从此只负责 `{% for todo in todos %}`，不再碰数据库。

更有意思的是 **app-5 → app-2 这一步**：到了 app-2，把 `conn.execute("INSERT INTO todo ...")` 换成 `db.add(Todo(...))`，**模板一字不动、路由结构一字不动**。学生亲手验证「换了底层数据库访问方式，界面纹丝不动」——这就是抽象层的价值。

```
app-6 → app-5 → app-2
 模板    路由    ORM
 即路由  分离    抽象
```

---

## 项目结构

```
app-5/
├── main.py                     # 入口：建表 → 注册路由 → 首页
├── config.py                   # DB_PATH = "todo-5.db"
├── database.py                 # raw sqlite3 连接 + get_db() 依赖注入
├── routers/
│   ├── __init__.py
│   └── todos.py                # 6 个端点，raw SQL
├── templates/
│   ├── index.html              # 列表 + 新增表单
│   └── edit.html               # 编辑页面
├── static/
│   └── css/style.css           # 样式
├── todo-5.db                   # SQLite 数据库（运行后生成）
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

与 app-6 对照——app-6 的每个操作都是独立 `.mako` 文件（`add.mako`、`add_db.mako`、`edit.mako`、`edit_db.mako`、`delete_db.mako`、`done_db.mako`），app-5 把它们全部收进 `routers/todos.py` 的 6 个函数里。

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r ../requirements.txt --break-system-packages
```

### 2. 运行

```bash
uvicorn app-5.main:app --host 0.0.0.0 --port 8005 --reload
```

### 3. 访问

| 页面 | 地址 |
|------|------|
| 首页 | http://localhost:8005 |
| API 文档 | http://localhost:8005/docs |

---

## 核心代码解读

### database.py — 依赖注入的雏形

```python
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 让查询结果支持 row['column'] 字典访问
    try:
        yield conn
    finally:
        conn.close()
```

`yield` 生成器 + `try/finally` 保证每次请求结束后连接一定关闭。签名和 app-2 的 SQLAlchemy 版 `get_db()` 完全一致——换 ORM 时路由代码不用改。

### routers/todos.py — SQL 的归宿

```python
@router.post("")
def create_todo(request: Request, info: str = Form(...), db=Depends(get_db)):
    db.execute("INSERT INTO todo (info, status) VALUES (?, 0)", (info,))
    db.commit()
    return RedirectResponse(url="/", status_code=303)
```

和 app-6 的 `add_db.mako` 完全相同的 SQL，但位置从模板搬到了路由函数。`Depends(get_db)` 自动注入连接，模板里不再有 `conn = sqlite3.connect(DB_PATH)`。

### 模板 — 终于只做渲染

```html
{% for todo in todos %}
<li class="todo-item{% if todo.status %} done{% endif %}">
    <span class="info">{{ todo.info }}</span>
    <div class="actions">
        <a href="/todos/{{ todo.id }}/toggle" class="btn btn-toggle">
            {{ '✓' if todo.status else '○' }}
        </a>
        <a href="/todos/{{ todo.id }}/edit" class="btn">编辑</a>
        <a href="/todos/{{ todo.id }}/delete"
           class="btn btn-delete"
           onclick="return confirm('确认删除？')">删除</a>
    </div>
</li>
{% endfor %}
```

对比 app-6 的 `list.mako`——`<% conn = sqlite3.connect(DB_PATH) %>` 消失了，只剩 `{% for todo in todos %}`。数据从路由传进来，模板不知道 SQL 是什么。

---

## SQL 对照表

这些 SQL 从 app-6 原样搬过来，只是执行位置从模板换到了路由函数：

| 操作 | SQL |
|------|-----|
| 查询全部 | `SELECT * FROM todo ORDER BY id DESC` |
| 查询单条 | `SELECT * FROM todo WHERE id = ?` |
| 插入 | `INSERT INTO todo (info, status) VALUES (?, 0)` |
| 更新 | `UPDATE todo SET info = ? WHERE id = ?` |
| 删除 | `DELETE FROM todo WHERE id = ?` |
| 切换状态 | `UPDATE todo SET status = 1 - COALESCE(status, 0) WHERE id = ?` |

到了 app-2，这些 SQL 全部换成 ORM 方法调用——但路由结构不变，模板不变。

---

## 演进路线

```
app-6/ → 模板即路由，Mako 混写 SQL
  ↓
app-5/ → 路由分离 + Jinja2，SQL 集中在路由层（当前版本）
  ↓
app-2/ → raw SQL 换成 SQLAlchemy ORM，模板和路由结构不变
  ↓
app-1/ → 加 HTMX 属性，实现零 JS 局部刷新
  ↓
app/   → 前后端分离，Vue.js SPA
  ↓
app+1/ → 架构分离，API 和前端独立部署
```

---

## 许可证

MIT License
