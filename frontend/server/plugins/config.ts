export default defineNitroPlugin((app) => {
    Object.defineProperty(global, '$config', {
        value: useRuntimeConfig(),
        writable: false
    })
})