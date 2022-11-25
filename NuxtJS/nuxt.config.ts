import { defineNuxtConfig } from 'nuxt';

// https://v3.nuxtjs.org/api/configuration/nuxt.config
export default defineNuxtConfig({
  modules: ['@nuxtjs/tailwindcss'],

  vite: {
    server: {
      host: "0.0.0.0",
      port: 3000,
      watch: { usePolling: true },
      hmr: {
        protocol: 'ws',
        host: 'localhost',
        port: 24678
      }
    }
  },

});
