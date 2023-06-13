import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0', // Replace with the desired host
    port: 80, // Replace with the desired port
    proxy: {
      "/backend/": {
        target: "http://127.0.0.1:8000",
        rewrite: (path) => path.replace(/^\/backend/, ""),
      },
    },
  },
})
