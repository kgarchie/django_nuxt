import { joinURL } from "ufo";

export default defineEventHandler(async event => {
    const path = event.path
    const proxy = useRuntimeConfig().public.apiBase || "http://localhost:8000"
    const target = joinURL(proxy, path)
    return await proxyRequest(event, target)
})