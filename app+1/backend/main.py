"""FastAPI 应用入口

app+1 版本特点：
- 前后端彻底分离，后端只提供 API
- 前端是独立的 Vue + Vite 工程
- 需要配置 CORS 允许前端跨域访问
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routers import todos

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建 FastAPI 实例
app = FastAPI(title="Todo API", version="1.0.0")

# 配置 CORS - 允许前端跨域访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite 开发服务器默认端口
        "http://localhost:3000",  # 备用端口
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(todos.router)


@app.get("/")
def root():
    """根路径 - 返回 API 信息"""
    return {
        "message": "Todo API",
        "docs": "/docs",
        "endpoints": "/api/todos"
    }
