<%
    todo_id = form.get('id', '')
    
    if todo_id:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("DELETE FROM todo WHERE id = ?", (todo_id,))
        conn.commit()
        conn.close()
    
    redirect('/list')
%>
