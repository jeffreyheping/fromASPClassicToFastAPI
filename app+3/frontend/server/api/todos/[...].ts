/**
 * BFF 代理层 - 代理所有 /api/todos 请求到 FastAPI 后端
 * 
 * 浏览器 → Nuxt (/api/todos) → FastAPI (localhost:8012/api/todos)
 *         ↑ 同源，无 CORS 问题
 */

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const backendUrl = config.backendUrl || 'http://localhost:8012'
  
  // 获取请求路径
  const path = event.path.replace('/api/', '')
  
  // 获取请求方法
  const method = event.method
  
  // 获取请求体（如果有）
  let body = null
  if (method !== 'GET' && method !== 'HEAD') {
    body = await readBody(event)
  }
  
  // 转发到后端
  try {
    const response = await $fetch(`${backendUrl}/api/${path}`, {
      method,
      body,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response
  } catch (error) {
    // 错误处理
    throw createError({
      statusCode: error.statusCode || 500,
      message: error.message || 'API 请求失败'
    })
  }
})
