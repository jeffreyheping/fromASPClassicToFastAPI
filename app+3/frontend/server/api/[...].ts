/**
 * BFF 代理层 - 代理所有 /api/* 请求到 FastAPI 后端
 * 
 * 浏览器 → Nuxt (/api/todos) → FastAPI (localhost:8012/api/todos)
 *         ↑ 同源，无 CORS 问题
 */

export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const backendUrl = config.backendUrl || 'http://localhost:8012'
  
  // 获取完整请求路径和方法
  const path = event.path
  const method = event.method
  
  // 获取请求体（如果有）
  let body = null
  if (method !== 'GET' && method !== 'HEAD') {
    body = await readBody(event)
  }
  
  // 转发到后端
  try {
    const response = await $fetch(`${backendUrl}${path}`, {
      method,
      body,
      headers: {
        'Content-Type': 'application/json'
      }
    })
    return response
  } catch (error: any) {
    throw createError({
      statusCode: error.statusCode || 500,
      message: error.message || 'API 请求失败'
    })
  }
})
