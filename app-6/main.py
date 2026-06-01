# -*- coding: utf-8 -*-
"""
app-6 — 退无可退版：Mako模板即路由 + sqlite3裸SQL

main.py 写一次就不改。
新增页面只需在 templates/ 下放 .mako 文件，刷新浏览器即可。

模板内可用的变量：
- request   : FastAPI 请求对象
- redirect(url) : 重定向
- DB_PATH   : 数据库路径
- sqlite3   : sqlite3 模块
"""
import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from mako.template import Template

from .config import DB_PATH, TEMPLATE_DIR, STATIC_DIR

# ---- 初始化数据库 ----
conn = sqlite3.connect(DB_PATH)
conn.execute('''CREATE TABLE IF NOT EXISTS todo (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    info TEXT NOT NULL,
    status INTEGER DEFAULT 0
)''')
conn.commit()
conn.close()

# ---- FastAPI 应用 ----
app = FastAPI(title="app-6 退无可退版")

# ---- 静态文件（必须在模板路由之前挂载）----
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# ---- 路由：一个兜底处理所有请求 ----
# URL 直接映射到 templates/ 下的 .mako 文件
# /list     -> templates/list.mako
# /add      -> templates/add.mako
# /         -> templates/index.mako

@app.get("/", response_class=HTMLResponse)
@app.post("/", response_class=HTMLResponse)
async def root(request: Request):
    return await page(request, "index")

@app.get("/{path:path}", response_class=HTMLResponse)
@app.post("/{path:path}", response_class=HTMLResponse)
async def page(request: Request, path: str):
    # 排除 static 路径（让 StaticFiles 处理）
    if path.startswith("static/"):
        return HTMLResponse(f"<h1>404 Not Found: /{path}</h1>", status_code=404)
    
    # 空路径处理
    if not path:
        path = "index"
    
    # 找模板文件
    template_file = os.path.join(TEMPLATE_DIR, path + ".mako")
    if not os.path.exists(template_file):
        return HTMLResponse(f"<h1>404 Not Found: /{path}</h1>", status_code=404)

    # 读取并渲染模板
    with open(template_file, "r", encoding="utf-8") as f:
        source = f.read()

    template = Template(source, filename=template_file)

    # redirect：模板内调用 redirect(url)，这里捕获并返回重定向响应
    class Redirect(Exception):
        def __init__(self, url):
            self.url = url

    def do_redirect(url):
        raise Redirect(url)

    # POST 请求时，预获取表单数据传给模板（模板内不能用 await）
    form_data = {}
    if request.method == "POST":
        form = await request.form()
        form_data = dict(form)

    try:
        html = template.render(
            request=request,
            redirect=do_redirect,
            DB_PATH=DB_PATH,
            sqlite3=sqlite3,
            form=form_data,  # 表单数据
            query=dict(request.query_params),  # URL参数
        )
    except Redirect as e:
        return RedirectResponse(e.url, status_code=303)

    return HTMLResponse(html)
