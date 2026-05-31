<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>编辑待办</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>编辑待办</h1>
    
    <%
        todo_id = query.get('id', '')
        
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        todo = conn.execute("SELECT * FROM todo WHERE id = ?", (todo_id,)).fetchone()
        conn.close()
    %>
    
    % if todo:
        <form method="POST" action="/edit_db">
            <input type="hidden" name="id" value="${todo['id']}">
            <textarea name="info" rows="4">${todo['info']}</textarea>
            <div class="form-actions">
                <a href="/list" class="btn">取消</a>
                <button type="submit" class="btn btn-primary">更新</button>
            </div>
        </form>
    % else:
        <p>待办不存在</p>
        <a href="/list">返回列表</a>
    % endif
</body>
</html>
