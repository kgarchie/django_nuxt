// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: true },
  runtimeConfig: {
    public: {
      apiBaseServer: 'http://localhost:8000',
      apiBaseClient: 'http://localhost:8000'
    }
  },
  modules: ['@nuxtjs/tailwindcss']
})
