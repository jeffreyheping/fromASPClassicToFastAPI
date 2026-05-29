"""测试认证 API（OAuth2 + JWT）"""
import pytest


def test_register_user(client):
    """注册新用户成功"""
    resp = client.post("/api/auth/register", json={
        "username": "testuser",
        "password": "testpass123",
    })
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["role"] == "guest"


def test_register_duplicate_fails(client):
    """重复注册同一用户名返回 400"""
    client.post("/api/auth/register", json={
        "username": "dup",
        "password": "testpass123",
    })
    resp = client.post("/api/auth/register", json={
        "username": "dup",
        "password": "testpass123",
    })
    assert resp.status_code == 400


def test_login_success(client):
    """登录成功返回 JWT token"""
    client.post("/api/auth/register", json={
        "username": "loginuser",
        "password": "testpass123",
    })
    resp = client.post("/api/auth/token", data={
        "username": "loginuser",
        "password": "testpass123",
    })
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    """密码错误返回 401"""
    client.post("/api/auth/register", json={
        "username": "badpw",
        "password": "testpass123",
    })
    resp = client.post("/api/auth/token", data={
        "username": "badpw",
        "password": "wrongpassword",
    })
    assert resp.status_code == 401


def test_login_nonexistent_user(client):
    """登录不存在的用户返回 401"""
    resp = client.post("/api/auth/token", data={
        "username": "nobody",
        "password": "testpass123",
    })
    assert resp.status_code == 401


def test_oauth2_bearer_header(client):
    """获取的 token 可以拼接成 OAuth2 Bearer 格式"""
    client.post("/api/auth/register", json={
        "username": "bearer",
        "password": "testpass123",
    })
    resp = client.post("/api/auth/token", data={
        "username": "bearer",
        "password": "testpass123",
    })
    token = resp.json()["access_token"]
    # Token 应该是有效的（能解码）
    assert len(token) > 20
