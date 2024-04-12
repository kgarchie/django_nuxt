export default defineEventHandler((context) => {
    if(!isVercel) console.info(`[${context.node.req.method}]\t${context.node.req.url}`)
})