import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    build: {
        outDir: "./../dist",
        chunkSizeWarningLimit: 1000,
    },
    plugins: [vue()],
});
