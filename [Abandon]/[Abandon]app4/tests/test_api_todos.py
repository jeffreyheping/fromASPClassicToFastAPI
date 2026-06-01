"""测试 Todo API（需认证的 JSON 端点）"""
import pytest


def _register_and_login(client, username="apitest", password="testpass123"):
    """辅助函数：注册 + 登录，返回 JWT token"""
    client.post("/api/auth/register", json={
        "username": username,
        "password": password,
    })
    resp = client.post("/api/auth/token", data={
        "username": username,
        "password": password,
    })
    return resp.json()["access_token"]


def _auth_headers(token):
    """拼接 OAuth2 Bearer header"""
    return {"Authorization": f"Bearer {token}"}


# ── 未认证访问 ──


def test_list_todos_without_auth(client):
    """未登录访问 todo API 返回 401"""
    resp = client.get("/api/todos")
    assert resp.status_code == 401


def test_create_todo_without_auth(client):
    """未登录创建 todo 返回 401"""
    resp = client.post("/api/todos", json={"info": "test"})
    assert resp.status_code == 401


# ── 已认证访问 ──


def test_create_todo(client):
    """认证后创建待办成功"""
    token = _register_and_login(client)
    resp = client.post("/api/todos", json={
        "info": "API测试事项",
    }, headers=_auth_headers(token))
    assert resp.status_code in (200, 201)
    data = resp.json()
    assert data["info"] == "API测试事项"
    assert data["id"] is not None


def test_list_todos(client):
    """认证后获取待办列表"""
    token = _register_and_login(client)
    client.post("/api/todos", json={"info": "事项1"}, headers=_auth_headers(token))
    client.post("/api/todos", json={"info": "事项2"}, headers=_auth_headers(token))

    resp = client.get("/api/todos", headers=_auth_headers(token))
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_todo(client):
    """更新待办内容"""
    token = _register_and_login(client)
    created = client.post("/api/todos", json={"info": "旧"}, headers=_auth_headers(token))
    todo_id = created.json()["id"]

    resp = client.put(f"/api/todos/{todo_id}", json={
        "info": "新内容",
    }, headers=_auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["info"] == "新内容"


def test_toggle_todo(client):
    """切换完成状态"""
    token = _register_and_login(client)
    created = client.post("/api/todos", json={"info": "事项"}, headers=_auth_headers(token))
    todo_id = created.json()["id"]

    resp = client.put(f"/api/todos/{todo_id}/toggle", headers=_auth_headers(token))
    assert resp.status_code == 200
    assert resp.json()["status"] == 1

    resp = client.put(f"/api/todos/{todo_id}/toggle", headers=_auth_headers(token))
    assert resp.json()["status"] == 0


def test_delete_todo(client):
    """删除待办"""
    token = _register_and_login(client)
    created = client.post("/api/todos", json={"info": "删除测试"}, headers=_auth_headers(token))
    todo_id = created.json()["id"]

    resp = client.delete(f"/api/todos/{todo_id}", headers=_auth_headers(token))
    assert resp.status_code == 200


def test_crud_flow(client):
    """完整 CRUD 流程：创建 → 读取 → 更新 → 删除 → 确认删除"""
    token = _register_and_login(client)
    headers = _auth_headers(token)

    # Create
    resp = client.post("/api/todos", json={"info": "流程测试"}, headers=headers)
    assert resp.status_code in (200, 201)
    todo_id = resp.json()["id"]

    # Read
    resp = client.get("/api/todos", headers=headers)
    assert len(resp.json()) == 1

    # Update
    resp = client.put(f"/api/todos/{todo_id}", json={"info": "已更新"}, headers=headers)
    assert resp.json()["info"] == "已更新"

    # Toggle
    resp = client.put(f"/api/todos/{todo_id}/toggle", headers=headers)
    assert resp.json()["status"] == 1

    # Delete
    resp = client.delete(f"/api/todos/{todo_id}", headers=headers)
    assert resp.status_code == 200

    # Verify deleted
    resp = client.get("/api/todos", headers=headers)
    assert len(resp.json()) == 0
