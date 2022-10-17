import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
    build: {
        outDir: "./../dist",
        chunkSizeWarningLimit: 1000,
    },
    base: process.env.ELECTRON == "true" ? "./" : ".",
    plugins: [vue()],
    server: {
        port: 3000,
    },
});
