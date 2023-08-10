import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import WindiCSS from 'vite-plugin-windicss';
import path from 'path';

export default defineConfig(({ mode }) => ({
    build: {
        outDir: mode == 'web' ? './../web/public/app' : './../dist',
        chunkSizeWarningLimit: 1000,
    },
    base: mode == 'development' ? '' : './',
    plugins: [vue(), WindiCSS()],
    server: {
        port: 3000,
    },
}));
