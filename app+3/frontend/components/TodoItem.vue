<template>
  <li class="todo-item" :class="{ completed: todo.status === 1 }">
    <span 
      class="todo-text" 
      :class="{ done: todo.status === 1 }"
      @click="$emit('toggle', todo.id)"
    >
      {{ todo.info }}
    </span>
    <div class="todo-actions">
      <button class="btn btn-sm" @click="$emit('edit', todo)">编辑</button>
      <button class="btn btn-sm btn-danger" @click="$emit('delete', todo.id)">删除</button>
    </div>
  </li>
</template>

<script setup lang="ts">
// Props 定义
interface Props {
  todo: {
    id: number
    info: string
    status: number
  }
}

defineProps<Props>()

// Emits 定义
defineEmits<{
  toggle: [id: number]
  edit: [todo: { id: number, info: string, status: number }]
  delete: [id: number]
}>()
</script>
