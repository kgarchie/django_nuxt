import type { APIResponse, UserState } from "~/typings";

export default defineNuxtPlugin(async (app) => {
    const user = useUser().value
    const token = getAuthToken()
    if (
        (
            !user ||
            isNone(user?.token) ||
            isNone(user?.email)
        ) &&
        (
            token &&
            isNone(token)
        )
    ) {
        const { execute } = await DeFetch<APIResponse>($config.public.apiBase + '/api/auth/refresh', {
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
                } else if (data.statusCode === 200) {
                    useUser().value = {
                        email: data.body.email,
                        token: token,
                        is_admin: data.body?.is_admin ?? false
                    }
                }
            },
            onResponseError({ error }) {
                console.error(error)
            }
        });

        await execute()
    }
})