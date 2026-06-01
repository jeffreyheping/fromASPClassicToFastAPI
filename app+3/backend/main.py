"""FastAPI 应用入口

app+3 版本特点：
- 前后端彻底分离，后端只提供 API
- 前端是 Nuxt 4 工程，带 SSR 和 BFF 层
- 不需要 CORS（BFF 同源代理）
"""
from fastapi import FastAPI

from database import engine, Base
from routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo API (app+3)", version="1.0.0")

# 不需要 CORS - BFF 层同源代理，浏览器不跨域

# 注册路由
app.include_router(todos.router)


@app.get("/")
def root():
    """根路径 - 返回 API 信息"""
    return {
        "message": "Todo API (app+3)",
        "docs": "/docs",
        "endpoints": "/api/todos"
    }
