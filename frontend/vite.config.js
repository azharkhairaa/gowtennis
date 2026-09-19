import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // GitHub Pages menyajikan situs di sub-path (/<nama-repo>/), sementara Surge
  // dan dev server memakai root. Workflow Pages mengisi VITE_BASE otomatis.
  base: process.env.VITE_BASE || '/',
  plugins: [vue()],
  server: {
    port: 5183,
    // Semua panggilan /api diteruskan ke FastAPI, jadi frontend tidak perlu
    // tahu host backend dan tidak ada urusan CORS saat pengembangan.
    proxy: {
      '/api': {
        target: process.env.VITE_API_TARGET || 'http://127.0.0.1:8010',
        changeOrigin: true,
      },
    },
  },
})
