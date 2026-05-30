/**
 * API 封装 - 统一管理后端接口调用
 * 
 * 前后端分离后，前端需要知道后端地址
 * 开发时通过 Vite 代理转发到后端，避免跨域问题
 */

const API_BASE = '/api'  // Vite 代理会把 /api 转发到后端

/**
 * 获取所有待办事项
 */
export async function getTodos() {
  const res = await fetch(`${API_BASE}/todos`)
  if (!res.ok) throw new Error('获取待办失败')
  return res.json()
}

/**
 * 新增待办事项
 */
export async function createTodo(info) {
  const res = await fetch(`${API_BASE}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ info })
  })
  if (!res.ok) throw new Error('创建待办失败')
  return res.json()
}

/**
 * 更新待办事项
 */
export async function updateTodo(id, info) {
  const res = await fetch(`${API_BASE}/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ info })
  })
  if (!res.ok) throw new Error('更新待办失败')
  return res.json()
}

/**
 * 切换完成状态
 */
export async function toggleTodoDone(id) {
  const res = await fetch(`${API_BASE}/todos/${id}/done`, {
    method: 'PUT'
  })
  if (!res.ok) throw new Error('切换状态失败')
  return res.json()
}

/**
 * 删除待办事项
 */
export async function deleteTodo(id) {
  const res = await fetch(`${API_BASE}/todos/${id}`, {
    method: 'DELETE'
  })
  if (!res.ok) throw new Error('删除待办失败')
  return res.json()
}
