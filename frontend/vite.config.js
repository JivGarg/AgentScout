import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Defaults to localhost for native `npm run dev`; docker-compose overrides
// this via the VITE_API_PROXY_TARGET env var to the `backend` service name.
const apiProxyTarget = process.env.VITE_API_PROXY_TARGET || 'http://localhost:8000';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    host: true,
    proxy: {
      '/api': {
        target: apiProxyTarget,
        changeOrigin: true,
      },
    },
  },
});
