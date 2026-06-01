<template>
  <ul class="todo-list">
    <TodoItem 
      v-for="todo in todos" 
      :key="todo.id" 
      :todo="todo"
      @toggle="$emit('toggle', $event)"
      @edit="$emit('edit', $event)"
      @delete="$emit('delete', $event)"
    />
  </ul>
  <p v-if="todos.length === 0" class="empty">暂无待办事项</p>
</template>

<script setup lang="ts">
// Props 定义
interface Props {
  todos: Array<{
    id: number
    info: string
    status: number
  }>
}

defineProps<Props>()

// Emits 定义
defineEmits<{
  toggle: [id: number]
  edit: [todo: { id: number, info: string, status: number }]
  delete: [id: number]
}>()
</script>
