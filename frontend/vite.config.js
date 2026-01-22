import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import { createHtmlPlugin } from "vite-plugin-html";
import vueDevTools from "vite-plugin-vue-devtools";
import { fileURLToPath, URL } from "node:url";
import eslint from "vite-plugin-eslint";
import pkg from "./package.json";

console.log("Vite config loaded");

export default defineConfig({
  plugins: [
    vue(),
    vueDevTools(),
    createHtmlPlugin({
      inject: {
        data: {
          title: "LenoreSchedule",
        },
      },
    }),
    eslint(),
  ],
  server: {
    proxy: {
      "/api": {
        target: "http://backend:8001/api", // Backend API server
        changeOrigin: true,
        rewrite: path => {
          console.log("proxy rewrite:", path);
          return path.replace(/^\/api/, "");
        },
      },
    },
    watch: {
      usePolling: true,
      interval: 300,
      ignored: [
        "**/node_modules/**",
        "**/.git/**",
        "**/dist/**",
        "**/__pycache__/**",
      ],
    },
  },
  define: {
    __VUE_OPTIONS_API__: true,
    __VUE_PROD_DEVTOOLS__: false,
    __VUE_PROD_HYDRATION_MISMATCH_DETAILS__: false,
    "import.meta.env.VITE_APP_VERSION": JSON.stringify(pkg.version),
  },
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
});
