export default defineEventHandler(async event => {
    const target = event.path
    return await proxyRequest(event, target)
})