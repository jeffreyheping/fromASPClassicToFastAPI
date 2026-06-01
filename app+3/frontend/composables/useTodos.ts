/**
 * useTodos - Todo 数据管理组合式函数
 * 
 * 使用 Nuxt 的 useFetch 实现 SSR 数据预取
 * - SSR 时：服务端预取数据，HTML 中包含完整内容
 * - CSR 时：客户端增量更新
 */

// Todo 类型定义
interface Todo {
  id: number
  info: string
  status: number  // 0=未完成, 1=已完成
}

export const useTodos = () => {
  // 获取待办列表 - useFetch 自动处理 SSR
  const { data: todos, pending: loading, error, refresh } = useFetch<Todo[]>('/api/todos')

  // 新增待办
  const addTodo = async (info: string) => {
    await $fetch('/api/todos', {
      method: 'POST',
      body: { info }
    })
    await refresh()
  }

  // 更新待办内容
  const updateTodo = async (id: number, info: string) => {
    await $fetch(`/api/todos/${id}`, {
      method: 'PUT',
      body: { info }
    })
    await refresh()
  }

  // 切换完成状态
  const toggleDone = async (id: number) => {
    await $fetch(`/api/todos/${id}/done`, {
      method: 'PUT'
    })
    await refresh()
  }

  // 删除待办
  const deleteTodo = async (id: number) => {
    await $fetch(`/api/todos/${id}`, {
      method: 'DELETE'
    })
    await refresh()
  }

  return {
    todos,
    loading,
    error,
    refresh,
    addTodo,
    updateTodo,
    toggleDone,
    deleteTodo
  }
}
