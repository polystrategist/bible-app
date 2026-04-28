import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import UnoCSS from 'unocss/vite';

export default defineConfig(({ mode }) => ({
    build: {
        outDir: mode == 'web' ? './../dist-web' : './../dist',
        chunkSizeWarningLimit: 2000,
    },
    // Electron loads via file:// so it needs './' relative paths.
    // Web is served from the site root, so '/'.
    base: mode == 'web' ? '/' : mode == 'development' ? '' : './',
    define: {
        __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
    },
    plugins: [vue(), UnoCSS()],
    server: {
        port: 3000,
    },
}));
