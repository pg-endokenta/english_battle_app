import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'
import { fileURLToPath } from 'url'

// __dirname 相当を定義（ESM対応）
const __filename = fileURLToPath(import.meta.url)
const __dirname = path.dirname(__filename)

export default defineConfig({
  plugins: [
    react(),
    tailwindcss()
  ],
  build: {
    outDir: '../backend/static/frontend',
    emptyOutDir: true,
    manifest: true,
    rollupOptions: {
      input: '/index.html',  // 明示的にindex.htmlをmanifestのキーに入れる
    },
  },
  base: '/static/frontend/',
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
})
