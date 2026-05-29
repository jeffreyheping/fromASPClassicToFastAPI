"""测试 services 业务逻辑层"""
from app4.core import services


def test_create_todo(db):
    """创建待办"""
    todo = services.create(db, "测试事项")
    assert todo.id is not None
    assert todo.info == "测试事项"
    assert todo.status == 0


def test_get_all_todos(db):
    """获取所有待办（倒序）"""
    services.create(db, "事项1")
    services.create(db, "事项2")
    todos = services.get_all(db)
    assert len(todos) == 2
    # 倒序：id 大的在前
    assert todos[0].id > todos[1].id


def test_get_by_id(db):
    """按 ID 查询"""
    todo = services.create(db, "事项")
    found = services.get_by_id(db, todo.id)
    assert found.info == "事项"


def test_get_by_id_not_found(db):
    """查询不存在的 ID 返回 None"""
    assert services.get_by_id(db, 999) is None


def test_update_info(db):
    """更新待办内容"""
    todo = services.create(db, "旧内容")
    updated = services.update_info(db, todo.id, "新内容")
    assert updated.info == "新内容"


def test_update_nonexistent(db):
    """更新不存在的待办返回 None"""
    assert services.update_info(db, 999, "内容") is None


def test_toggle_status(db):
    """切换完成状态"""
    todo = services.create(db, "事项")
    assert todo.status == 0

    toggled = services.toggle_status(db, todo.id)
    assert toggled.status == 1

    toggled = services.toggle_status(db, todo.id)
    assert toggled.status == 0


def test_delete_todo(db):
    """删除待办"""
    todo = services.create(db, "事项")
    assert services.delete(db, todo.id) is True
    assert services.get_by_id(db, todo.id) is None


def test_delete_nonexistent(db):
    """删除不存在的待办返回 False"""
    assert services.delete(db, 999) is False
