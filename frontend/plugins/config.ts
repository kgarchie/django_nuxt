export default defineNuxtPlugin((app) => {
    if (window?.$config) return;
    if (process.client) window.$config = app.$config;
})