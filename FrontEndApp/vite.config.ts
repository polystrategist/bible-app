import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import UnoCSS from 'unocss/vite';

export default defineConfig(({ mode }) => ({
    build: {
        outDir: mode == 'web' ? './../web/public/app' : './../dist',
        chunkSizeWarningLimit: 2000,
    },
    base: mode == 'web' ? '/app/' : mode == 'development' ? '' : './',
    plugins: [vue(), UnoCSS()],
    server: {
        port: 3000,
    },
}));
