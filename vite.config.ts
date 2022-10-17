import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import WindiCSS from 'vite-plugin-windicss';

// https://vitejs.dev/config/
export default defineConfig({
    base: process.env.ELECTRON == 'true' ? './' : '',
    plugins: [vue(), WindiCSS()],
});
