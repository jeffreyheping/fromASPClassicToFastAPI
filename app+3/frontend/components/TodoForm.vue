<template>
  <div class="form-view">
    <h2>{{ isEdit ? '编辑待办' : '新增待办' }}</h2>
    <textarea 
      v-model="info" 
      placeholder="输入待办事项..." 
      rows="4"
    ></textarea>
    <div class="form-actions">
      <button class="btn" @click="$emit('cancel')">取消</button>
      <button class="btn btn-primary" @click="handleSubmit">
        {{ isEdit ? '更新' : '保存' }}
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
// Props 定义
interface Props {
  initialInfo?: string
  isEdit?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  initialInfo: '',
  isEdit: false
})

// Emits 定义
const emit = defineEmits<{
  submit: [info: string]
  cancel: []
}>()

// 表单数据
const info = ref(props.initialInfo)

// 提交处理
const handleSubmit = () => {
  const trimmed = info.value.trim()
  if (!trimmed) {
    alert('请输入内容')
    return
  }
  emit('submit', trimmed)
}

// 监听 initialInfo 变化（编辑模式）
watch(() => props.initialInfo, (newVal) => {
  info.value = newVal
})
</script>
