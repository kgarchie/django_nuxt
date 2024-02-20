import type { UseFetchOptions } from "#app";

export async function DeezFetch<T>(url: string | Ref, options?: UseFetchOptions<T>) {
    return useFetch<T>(url, {
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            "Authorization": "Bearer " + getAuthToken() || ""
        },
        watch: false,
        immediate: false,
        ...options as any
    })
}