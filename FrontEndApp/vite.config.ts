import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import WindiCSS from "vite-plugin-windicss";

export default defineConfig(({ mode }) => ({
    build: {
        outDir: "./../dist",
        chunkSizeWarningLimit: 1000,
    },
    base: mode == "development" ? "" : "./",
    plugins: [vue(), WindiCSS()],
    server: {
        port: 3000,
    },
}));
