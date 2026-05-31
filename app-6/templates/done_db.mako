<%
    todo_id = query.get('id', '')
    
    if todo_id:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("UPDATE todo SET status = 1 - COALESCE(status, 0) WHERE id = ?", (todo_id,))
        conn.commit()
        conn.close()
    
    redirect('/list')
%>
