<script>
/**
 * Todo App - Vue 3 组件（Options API）
 * 
 * 从 app/ 的 app.js 迁移而来，使用 Vite 构建工具
 * 前后端分离后，通过 api.js 调用后端接口
 */
import { getTodos, createTodo, updateTodo, toggleTodoDone, deleteTodo } from './api.js'

export default {
  name: 'App',
  data() {
    return {
      view: 'list',      // 当前视图：list | add | edit
      todos: [],         // 待办列表
      form: { info: '' }, // 表单数据
      editingId: null,   // 正在编辑的待办ID
      loading: false,    // 加载状态
      error: null        // 错误信息
    }
  },
  mounted() {
    // 组件挂载后自动加载数据
    this.loadTodos()
  },
  methods: {
    // 加载所有待办
    async loadTodos() {
      this.loading = true
      this.error = null
      try {
        this.todos = await getTodos()
      } catch (err) {
        this.error = '加载失败：' + err.message
      } finally {
        this.loading = false
      }
    },

    // 切换完成状态
    async toggleDone(id) {
      try {
        await toggleTodoDone(id)
        await this.loadTodos()
      } catch (err) {
        alert('操作失败：' + err.message)
      }
    },

    // 进入编辑模式
    editTodo(todo) {
      this.editingId = todo.id
      this.form.info = todo.info
      this.view = 'edit'
    },

    // 进入新增模式
    showAdd() {
      this.form.info = ''
      this.view = 'add'
    },

    // 取消操作，返回列表
    cancel() {
      this.form.info = ''
      this.editingId = null
      this.view = 'list'
    },

    // 新增待办
    async saveAdd() {
      const info = this.form.info.trim()
      if (!info) {
        alert('请输入内容')
        return
      }
      try {
        await createTodo(info)
        this.form.info = ''
        this.view = 'list'
        await this.loadTodos()
      } catch (err) {
        alert('创建失败：' + err.message)
      }
    },

    // 更新待办
    async saveEdit() {
      const info = this.form.info.trim()
      if (!info) {
        alert('请输入内容')
        return
      }
      try {
        await updateTodo(this.editingId, info)
        this.form.info = ''
        this.editingId = null
        this.view = 'list'
        await this.loadTodos()
      } catch (err) {
        alert('更新失败：' + err.message)
      }
    },

    // 删除待办
    async removeTodo(id) {
      if (!confirm('确定要删除吗？')) return
      try {
        await deleteTodo(id)
        await this.loadTodos()
      } catch (err) {
        alert('删除失败：' + err.message)
      }
    }
  }
}
</script>

<template>
  <div class="container">
    <h1>Todo App（Vue + Vite 版）</h1>
    <p class="subtitle">前后端分离架构演示</p>

    <!-- 加载中 -->
    <div v-if="loading" class="loading">加载中...</div>

    <!-- 错误提示 -->
    <div v-if="error" class="error">{{ error }}</div>

    <!-- 列表视图 -->
    <div v-if="view === 'list' && !loading">
      <div class="actions">
        <button class="btn btn-primary" @click="showAdd">+ 新增待办</button>
      </div>

      <ul class="todo-list">
        <li v-for="todo in todos" :key="todo.id" class="todo-item">
          <span 
            class="todo-text" 
            :class="{ done: todo.status }"
            @click="toggleDone(todo.id)"
          >
            {{ todo.info }}
          </span>
          <div class="todo-actions">
            <button class="btn btn-sm" @click="editTodo(todo)">编辑</button>
            <button class="btn btn-sm btn-danger" @click="removeTodo(todo.id)">删除</button>
          </div>
        </li>
      </ul>

      <p v-if="todos.length === 0" class="empty">暂无待办事项</p>
    </div>

    <!-- 新增视图 -->
    <div v-if="view === 'add'" class="form-view">
      <h2>新增待办</h2>
      <textarea 
        v-model="form.info" 
        placeholder="输入待办事项..."
        rows="4"
      ></textarea>
      <div class="form-actions">
        <button class="btn" @click="cancel">取消</button>
        <button class="btn btn-primary" @click="saveAdd">保存</button>
      </div>
    </div>

    <!-- 编辑视图 -->
    <div v-if="view === 'edit'" class="form-view">
      <h2>编辑待办</h2>
      <textarea 
        v-model="form.info" 
        placeholder="输入待办事项..."
        rows="4"
      ></textarea>
      <div class="form-actions">
        <button class="btn" @click="cancel">取消</button>
        <button class="btn btn-primary" @click="saveEdit">更新</button>
      </div>
    </div>
  </div>
</template>

<style>
/* 基础样式 */
* {
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  margin: 0;
  padding: 20px;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h1 {
  margin: 0 0 5px 0;
  color: #333;
}

.subtitle {
  color: #666;
  font-size: 14px;
  margin: 0 0 20px 0;
}

/* 按钮样式 */
.btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn:hover {
  background: #f0f0f0;
}

.btn-primary {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.btn-primary:hover {
  background: #0056b3;
}

.btn-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background: #dc3545;
  color: white;
}

.btn-sm {
  padding: 4px 12px;
  font-size: 12px;
}

/* 列表样式 */
.actions {
  margin-bottom: 20px;
}

.todo-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  border-bottom: 1px solid #eee;
}

.todo-item:last-child {
  border-bottom: none;
}

.todo-text {
  flex: 1;
  cursor: pointer;
  padding: 4px;
}

.todo-text:hover {
  background: #f0f0f0;
  border-radius: 4px;
}

.todo-text.done {
  text-decoration: line-through;
  color: #999;
}

.todo-actions {
  display: flex;
  gap: 8px;
}

.empty {
  text-align: center;
  color: #999;
  padding: 40px;
}

/* 表单样式 */
.form-view {
  margin-top: 20px;
}

.form-view h2 {
  margin: 0 0 15px 0;
  font-size: 18px;
}

textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  resize: vertical;
  font-family: inherit;
}

.form-actions {
  margin-top: 15px;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

/* 状态提示 */
.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.error {
  background: #f8d7da;
  color: #721c24;
  padding: 12px;
  border-radius: 4px;
  margin-bottom: 15px;
}
</style>
