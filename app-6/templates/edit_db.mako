<%
    todo_id = form.get('id', '')
    info = form.get('info', '').strip()
    
    if todo_id and info:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE todo SET info = ? WHERE id = ?", (info, todo_id))
        conn.commit()
        conn.close()
    
    redirect('/list')
%>
