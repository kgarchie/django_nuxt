// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  },
  modules: ['@nuxtjs/tailwindcss']
})
