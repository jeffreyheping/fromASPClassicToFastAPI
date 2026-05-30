import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      // 开发时，把 /api 请求转发到后端
      '/api': {
        target: 'http://localhost:8010',  // FastAPI 后端地址
        changeOrigin: true,
      }
    }
  }
})
