import type { APIResponse, UserState } from "~/typings"

export function setAuthCookie(token: string, expiry?: number) {
    const expires = expiry ? new Date(Date.now() + expiry * 1000) : undefined
    const cookie = useCookie<string>("auth", {
        expires: expires
    })
    cookie.value = token
}


export function getAuthCookie(): string | null {
    const cookie = useCookie<string>("auth").value?.trim()
    if (
        !cookie ||
        cookie === "undefined" ||
        cookie === "null" ||
        cookie === "false" ||
        cookie === ""
    ) return null

    return useCookie<string>("auth").value
}

export function getAuthToken() {
    const state = useUser()?.value?.token?.trim()
    const cookie = getAuthCookie()

    if (
        !state ||
        state === "undefined" ||
        state === "null" ||
        state === "false" ||
        state === ""
    ) return cookie
    return state
}

export function userIsAuthenticated() {
    return !!getAuthToken()
}

export function logout() {
    $fetch<APIResponse>("/api/auth/logout", {
        headers: {
            "Authorization": "Bearer " + getAuthToken(),
        },
        async onResponse({ response }) {
            if (response._data.statusCode === 200) {
                const state = useUser()
                state.value = {} as UserState
                setAuthCookie("", 0)
                await navigateTo("/login")
            } else {
                console.error(response)
            }
        },
        onRequestError(error) {
            console.error(error)
        }
    })
}

export async function assertAuth(redirect: string) {
    if (!userIsAuthenticated()) {
        await navigateTo("/login?redirect=" + redirect)
    }
}

export function getCSRFToken(){
    const token = useCookie('csrftoken').value
    return token?.toString() || ''
}