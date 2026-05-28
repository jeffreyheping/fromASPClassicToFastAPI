# Todo FastAPI + HTMX 搭建指南

> 照做一定成功版 · 2026 年 5 月

---

## 一、准备工作

### 1.1 确认环境

确保已安装：
- Python 3.10 或更高版本
- pip（Python 包管理器）

验证：
```bash
python3 --version
pip3 --version
```

### 1.2 进入项目目录

```bash
cd /workspace/todo_fastapi_one_1/app-1
```

---

## 二、安装依赖

使用项目根目录的 `requirements.txt`（版本已锁定）：

```bash
pip install -r ../requirements.txt --break-system-packages
```

---

## 三、项目文件说明

本目录已包含完整代码，文件清单：

```
app-1/
├── __init__.py              # 空文件
├── config.py                # 数据库配置
├── database.py              # SQLAlchemy 引擎和会话
├── models.py                # Todo 数据模型
├── main.py                  # FastAPI 入口（6个路由端点）
├── templates/
│   ├── index.html           # 主页面（内联CSS + HTMX）
│   └── partials/
│       ├── todo_list.html   # 待办列表片段
│       └── edit_form.html   # 编辑表单片段
├── README.md                # 项目说明
└── SETUP.md                 # 本文件
```

---

## 四、运行项目

```bash
uvicorn app-1.main:app --host 0.0.0.0 --port 8003 --reload
```

看到以下输出表示启动成功：
```
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

打开浏览器访问：http://localhost:8003

---

## 五、验证功能

### 测试步骤

| 步骤 | 操作 | 预期结果 |
|------|------|---------|
| 1 | 在输入框输入内容，点击「+ 新增」 | 待办出现在列表中，输入框清空 |
| 2 | 点击待办文字 | 文字出现删除线（已完成） |
| 3 | 再次点击待办文字 | 删除线消失（未完成） |
| 4 | 点击 ✏️ | 该行变成编辑表单 |
| 5 | 修改内容，点击「保存」 | 列表更新，显示新内容 |
| 6 | 点击 🗑️ | 弹出确认框，确认后待办被删除 |

### HTMX 效果观察

打开浏览器开发者工具（F12）→ Network 标签：

1. 点击「+ 新增」时，会看到 POST 请求发送到 `/todos`
2. 后端返回 HTML 片段（不是 JSON）
3. HTMX 自动将返回的 HTML 替换到 `#todo-list` 元素

---

## 六、核心代码解析

### 6.1 main.py 路由端点

```python
@app.post("/todos")
def create_todo(
    request: Request,
    info: str = Form(...),  # 接收表单数据
    db: Session = Depends(get_db)
):
    """HTMX: 新增待办"""
    todo = Todo(info=info)
    db.add(todo)
    db.commit()
    
    # 返回 HTML 片段，不是 JSON！
    todos = db.query(Todo).order_by(Todo.id.desc()).all()
    return templates.TemplateResponse("partials/todo_list.html", {
        "request": request,
        "todos": todos
    })
```

### 6.2 index.html 中的 HTMX 属性

```html
<!-- 新增表单 -->
<form hx-post="/todos"           <!-- POST 请求 -->
      hx-target="#todo-list"     <!-- 更新目标元素 -->
      hx-swap="innerHTML"        <!-- 替换内部内容 -->
      hx-on::after-request="this.reset()">  <!-- 提交后清空表单 -->
    <input type="text" name="info" placeholder="输入待办事项..." required>
    <button type="submit" class="btn btn-primary">+ 新增</button>
</form>

<!-- 待办列表容器 -->
<div id="todo-list">
    {% include "partials/todo_list.html" %}
</div>
```

### 6.3 todo_list.html 片段

```html
<ul class="todo-list">
    {% for todo in todos %}
    <li class="{% if todo.status == 1 %}done{% endif %}">
        <!-- 点击文字切换完成状态 -->
        <span class="info"
              hx-put="/todos/{{ todo.id }}/toggle"
              hx-target="#todo-list"
              hx-swap="innerHTML">
            {{ todo.info }}
        </span>
        <span class="actions">
            <!-- 编辑按钮 -->
            <button class="btn btn-sm"
                    hx-get="/todos/{{ todo.id }}/edit"
                    hx-target="closest li"
                    hx-swap="outerHTML">
                ✏️
            </button>
            <!-- 删除按钮 -->
            <button class="btn btn-sm btn-danger"
                    hx-delete="/todos/{{ todo.id }}"
                    hx-target="#todo-list"
                    hx-swap="innerHTML"
                    hx-confirm="确定要删除吗？">
                🗑️
            </button>
        </span>
    </li>
    {% endfor %}
</ul>
```

---

## 七、与 Vue 版本的关键区别

### 数据流对比

**Vue 版本**：
```
用户点击 → Vue 方法 → fetch API → JSON 响应 → 更新 data → Vue 重新渲染
```

**HTMX 版本**：
```
用户点击 → HTMX 发送请求 → HTML 片段响应 → HTMX 替换 DOM
```

### 代码位置对比

| 功能 | Vue 版本 | HTMX 版本 |
|------|---------|----------|
| 新增待办 | `app.js` 中的 `saveAdd()` 方法 | `main.py` 中的 `create_todo()` 路由 |
| 渲染列表 | Vue 的 `v-for` 指令 | Jinja2 模板 `{% for %}` |
| 切换完成 | `app.js` 中的 `toggleDone()` | `main.py` 中的 `toggle_todo()` 路由 |
| 更新页面 | Vue 响应式更新 | HTMX 替换 HTML 片段 |

---

## 八、常见问题

### Q1: 页面刷新后数据丢失

**原因**：HTMX 版本和 Vue 版本使用不同的数据库文件。

**解决**：这是设计如此。`app/` 使用 `todo.db`，`app-1/` 使用 `todo_htmx.db`。

### Q2: 点击待办文字没有反应

**检查**：查看浏览器控制台是否有 JavaScript 错误。

**解决**：确保 HTMX CDN 加载成功：
```html
<script src="https://unpkg.com/htmx.org@1.9.10"></script>
```

### Q3: 如何调试 HTMX 请求

**方法**：在浏览器开发者工具中：
1. Network 标签查看请求/响应
2. Console 标签执行 `htmx.logAll()` 查看详细日志

### Q4: 与 Vue 版本同时运行会冲突吗

**不会**：两个版本使用不同的端口：
- Vue 版本：http://localhost:8000
- HTMX 版本：http://localhost:8003

可以同时运行，互不影响。

---

## 九、学习建议

### 对比学习法

1. 先完整体验 HTMX 版本的所有功能
2. 再体验 Vue 版本的相同功能
3. 对比两者的代码差异：
   - 同样点击「新增」，代码在哪里？
   - 同样显示列表，数据怎么来的？
   - 同样切换完成，请求怎么发的？

### 思考问题

1. 为什么 HTMX 版本不需要 `app.js`？
2. 为什么 HTMX 版本返回 HTML 而不是 JSON？
3. 什么时候应该用 HTMX，什么时候应该用 Vue？

---

## 十、下一步

完成本版本学习后：

1. **阅读根目录 README.md** - 了解整个项目的架构
2. **对比 Vue 版本代码** - 理解两种实现方式的优劣
3. **尝试添加功能** - 比如搜索、分页、分类
4. **思考演进路径** - 从 HTMX → Vue → 前后端完全分离

---

> **HTMX 哲学**：
> 
> "The future of web development is not JavaScript. It's HTML."
> 
> —— HTMX 官网
