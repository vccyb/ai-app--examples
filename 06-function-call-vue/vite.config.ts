import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss()],
  server: {
    proxy: {
      '/history': { target: 'http://localhost:3000', changeOrigin: true },
      '/fc': { target: 'http://localhost:3000', changeOrigin: true },
      '/fc-sse': { target: 'http://localhost:3000', changeOrigin: true }
    }
  }
})