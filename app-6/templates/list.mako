<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Todo 列表</title>
    <link rel="stylesheet" href="/static/css/style.css">
</head>
<body>
    <h1>Todo 列表</h1>
    
    <%
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        todos = conn.execute("SELECT * FROM todo ORDER BY id DESC").fetchall()
        conn.close()
    %>
    
    % if len(todos) == 0:
        <p class="empty">暂无待办事项</p>
    % else:
        % for todo in todos:
            <div class="todo-item ${'completed' if todo['status'] == 1 else ''}">
                <span>
                    % if todo['status'] == 1:
                        <span class="status-done">[已完成]</span>
                    % else:
                        <span class="status-todo">[待办]</span>
                    % endif
                    <span class="todo-text">${todo['info']}</span>
                </span>
                <span class="actions">
                    <a href="/done_db?id=${todo['id']}">
                        ${'取消完成' if todo['status'] == 1 else '标记完成'}
                    </a>
                    <a href="/edit?id=${todo['id']}">编辑</a>
                    <form method="POST" action="/delete_db" style="display:inline">
                        <input type="hidden" name="id" value="${todo['id']}">
                        <a href="javascript:void(0)"
                           onclick="if(confirm('确定删除该待办？'))this.closest('form').submit()">
                           删除
                        </a>
                    </form>
                </span>
            </div>
        % endfor
    % endif
    
    <a href="/add" class="add-btn">+ 新增待办</a>
</body>
</html>
