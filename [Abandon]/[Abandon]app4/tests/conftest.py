"""pytest fixtures - 共享的测试基础设施"""
import os

# ⚠️ 必须在任何 app4 模块导入之前设置环境变量！
os.environ["APP4_DATABASE_URL"] = "sqlite:///:memory:"
os.environ["APP4_SECRET_KEY"] = "test-secret-key"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app4.core.database import Base, get_db

# 测试专用 engine（in-memory，StaticPool 确保所有连接共享同一个内存库）
test_engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


def override_get_db():
    """替换 FastAPI 的 get_db 依赖，使用测试数据库"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(autouse=True)
def setup_db():
    """每个测试前后：建表 / 清表"""
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    """直接获取测试数据库 session（测试 services 层用）"""
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    """FastAPI TestClient（已注入测试数据库）"""
    from app4.main import create_app

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as client:
        yield client
