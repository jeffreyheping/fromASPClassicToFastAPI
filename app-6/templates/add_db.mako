<%
    info = form.get('info', '').strip()
    
    if info:
        conn = sqlite3.connect(DB_PATH)
        conn.execute("INSERT INTO todo (info, status) VALUES (?, 0)", (info,))
        conn.commit()
        conn.close()
    
    redirect('/list')
%>
