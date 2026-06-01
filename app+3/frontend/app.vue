<template>
  <div>
    <NuxtPage />
  </div>
</template>

<script setup>
// 根组件 - 页面布局容器
useHead({
  title: 'Todo App (Nuxt 4)',
  meta: [
    { name: 'description', content: 'FastAPI + Nuxt 4 Todo 应用' }
  ]
})
</script>

<style>
/* 全局样式 */
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background: #f5f5f5;
  color: #333;
  line-height: 1.6;
}

.container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

h1 {
  margin-bottom: 10px;
  color: #333;
}

.subtitle {
  color: #666;
  margin-bottom: 20px;
  font-size: 14px;
}

/* 按钮样式 */
.btn {
  display: inline-block;
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  text-decoration: none;
  color: #333;
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

.btn-sm {
  padding: 4px 8px;
  font-size: 12px;
}

.btn-danger {
  color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background: #dc3545;
  color: white;
}

/* 待办列表 */
.todo-list {
  list-style: none;
  margin: 20px 0;
}

.todo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px;
  background: white;
  border-radius: 4px;
  margin-bottom: 8px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.todo-item.completed .todo-text {
  text-decoration: line-through;
  color: #999;
}

.todo-text {
  cursor: pointer;
  flex: 1;
}

.todo-text.done {
  color: #28a745;
}

.todo-actions {
  display: flex;
  gap: 8px;
}

/* 空状态 */
.empty {
  text-align: center;
  color: #999;
  padding: 40px;
}

/* 表单样式 */
.form-view {
  background: white;
  padding: 20px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.form-view h2 {
  margin-bottom: 15px;
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

/* 加载状态 */
.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

/* 错误提示 */
.error {
  color: #dc3545;
  padding: 10px;
  background: #ffe6e6;
  border-radius: 4px;
  margin: 10px 0;
}

/* 操作区 */
.actions {
  margin-bottom: 20px;
}

/* 信息框 */
.info-box {
  margin-top: 30px;
  padding: 15px;
  background: #e7f3ff;
  border-radius: 4px;
  font-size: 14px;
  color: #0066cc;
}

.info-box code {
  background: #fff;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 13px;
}
</style>
