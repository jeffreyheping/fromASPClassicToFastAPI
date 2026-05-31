<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>新增待办</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>新增待办</h1>
    
    <form method="POST" action="/add_db">
        <textarea name="info" rows="4" placeholder="输入待办事项..."></textarea>
        <div class="form-actions">
            <a href="/list" class="btn">取消</a>
            <button type="submit" class="btn btn-primary">保存</button>
        </div>
    </form>
</body>
</html>
