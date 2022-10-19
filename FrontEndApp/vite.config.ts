import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig(({ mode }) => ({
    build: {
        outDir: "./../dist",
        chunkSizeWarningLimit: 1000,
    },
    base: mode == "development" ? "" : "./",
    plugins: [vue()],
    server: {
        port: 3000,
    },
}));
