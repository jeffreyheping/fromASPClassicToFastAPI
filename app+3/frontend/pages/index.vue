<template>
  <div class="container">
    <h1>待办事项（Nuxt 4 SSR 版）</h1>
    <p class="subtitle">服务端渲染 + 文件路由 + BFF 代理</p>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 列表视图 -->
    <div v-if="view === 'list' && !loading">
      <div class="actions">
        <button class="btn btn-primary" @click="showAdd">+ 新增待办</button>
      </div>
      <TodoList 
        :todos="todos || []"
        @toggle="handleToggle"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>

    <!-- 新增视图 -->
    <TodoForm 
      v-if="view === 'add'"
      @submit="handleAdd"
      @cancel="view = 'list'"
    />

    <!-- 编辑视图 -->
    <TodoForm 
      v-if="view === 'edit'"
      :initial-info="editingTodo?.info || ''"
      :is-edit="true"
      @submit="handleUpdate"
      @cancel="cancelEdit"
    />

    <!-- 信息框 -->
    <div class="info-box">
      <strong>Nuxt 4 版：</strong>
      SSR 服务端渲染（首屏快、SEO 友好）+ 文件路由（pages/ 目录即路由）+ BFF 代理（同源无 CORS）。
      <code>useFetch</code> 自动处理 SSR 数据预取。
    </div>
  </div>
</template>

<script setup lang="ts">
// 使用 useTodos 组合式函数
const { 
  todos, 
  loading, 
  error, 
  addTodo, 
  updateTodo, 
  toggleDone, 
  deleteTodo 
} = useTodos()

// 视图状态
const view = ref<'list' | 'add' | 'edit'>('list')
const editingTodo = ref<{ id: number, info: string, status: number } | null>(null)

// 显示新增表单
const showAdd = () => {
  view.value = 'add'
}

// 处理新增
const handleAdd = async (info: string) => {
  await addTodo(info)
  view.value = 'list'
}

// 处理编辑
const handleEdit = (todo: { id: number, info: string, status: number }) => {
  editingTodo.value = todo
  view.value = 'edit'
}

// 处理更新
const handleUpdate = async (info: string) => {
  if (editingTodo.value) {
    await updateTodo(editingTodo.value.id, info)
    editingTodo.value = null
    view.value = 'list'
  }
}

// 取消编辑
const cancelEdit = () => {
  editingTodo.value = null
  view.value = 'list'
}

// 处理切换状态
const handleToggle = async (id: number) => {
  await toggleDone(id)
}

// 处理删除
const handleDelete = async (id: number) => {
  if (confirm('确定要删除吗？')) {
    await deleteTodo(id)
  }
}
</script>
