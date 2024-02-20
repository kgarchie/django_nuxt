import type { APIResponse, UserState } from "~/typings";

export default defineNuxtPlugin(async (app) => {
    const user = useUser().value
    const token = getAuthToken()
    if (
        (
            !user ||
            !user?.token ||
            user?.token?.trim() === "undefined" ||
            user?.token?.trim() === "null" ||
            user?.token?.trim() === "false" ||
            user?.token?.trim() === "" ||
            !user?.email ||
            !user?.email?.trim() ||
            user?.email?.trim() === "undefined" ||
            user?.email?.trim() === "null" ||
            user?.email?.trim() === "false" ||
            user?.email?.trim() === ""
        ) &&
        (
            token &&
            token.trim() !== "undefined" &&
            token.trim() !== "null" &&
            token.trim() !== "false" &&
            token.trim() !== ""
        )
    ) {
        const { execute, data } = await DeezFetch<APIResponse>($config.public.apiBase + '/api/auth/refresh', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            onResponse({ response }) {
                const data = response._data as APIResponse
                if (data.statusCode !== 200) {
                    setAuthCookie("", 0)
                    useUser().value = {} as UserState
                }
            },
            onResponseError({ error }) {
                console.error(error)
            }
        });

        await execute()

        const { value } = data
        if(value && value.statusCode === 200) {
            console.log(value.body)
            useUser().value = {
                email: value.body.email,
                token: token,
                is_admin: value.body?.is_admin || false
            }
        }
    }
})