<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Todo App - 模板即路由</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
<div class="container">
    <h1>📋 待办事项（模板即路由）</h1>
    <p class="subtitle">Python + SQL + HTML 全写在一个文件——最原始也最直观的 Web 开发</p>
    
    <%
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        todos = conn.execute("SELECT * FROM todo ORDER BY id DESC").fetchall()
        conn.close()
    %>
    
    <div class="actions">
        <a href="/add" class="btn btn-primary">+ 新增待办</a>
    </div>
    
    % if len(todos) == 0:
        <p class="empty">暂无待办事项</p>
    % else:
        <ul class="todo-list">
        % for todo in todos:
            <li class="todo-item">
                <span class="todo-text ${'done' if todo['status'] == 1 else ''}">${todo['info']}</span>
                <span class="todo-actions">
                    <a href="/done_db?id=${todo['id']}" class="btn btn-sm">
                        ${'取消完成' if todo['status'] == 1 else '标记完成'}
                    </a>
                    <a href="/edit?id=${todo['id']}" class="btn btn-sm">编辑</a>
                    <form method="POST" action="/delete_db" style="display:inline">
                        <input type="hidden" name="id" value="${todo['id']}">
                        <button type="submit" class="btn btn-sm btn-danger"
                            onclick="return confirm('确定要删除吗？')">删除</button>
                    </form>
                </span>
            </li>
        % endfor
        </ul>
    % endif
</div>

<div class="info-box">
    <strong>💡 模板即路由版：</strong>
    Python + SQL + HTML 全写在 <code>.mako</code> 模板文件里。<br>
    新建一个模板 = 新增一个页面，刷新即可看到效果。<br>
    <code>main.py</code> 是黑盒，写一次不再改 —— 你只和 <code>templates/</code> 打交道。<br>
    下一站：<a href="http://localhost:8005">app-5（路由分离版）</a> — 把 SQL 从模板搬到路由函数。
</div>
</body>
</html>
