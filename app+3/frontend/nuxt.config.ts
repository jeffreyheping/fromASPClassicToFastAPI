// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  
  // SSR 配置
  ssr: true,
  
  // 开发服务器配置
  devServer: {
    port: 3000
  },
  
  // 运行时配置
  runtimeConfig: {
    // 后端 API 地址（服务端使用）
    backendUrl: 'http://localhost:8012',
    // 公开配置（客户端也可访问）
    public: {
      apiBase: '/api'
    }
  },
  
  // Nitro 配置（服务端引擎）
  nitro: {
    // 开发时的代理配置
    devProxy: {
      '/api': {
        target: 'http://localhost:8012',
        changeOrigin: true
      }
    }
  }
})
