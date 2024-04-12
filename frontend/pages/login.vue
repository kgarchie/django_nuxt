<script setup lang="ts">
import type { APIResponse } from '~/typings';

const url = useRoute()
let redirect = url.query?.redirect
const remember = ref(false)
const loading = ref(false)
const errors = ref(new Set<string>())
const details = reactive({
    email: '',
    password: ''
})

const { execute } = await unFetch('/api/auth/login', {
    method: 'POST',
    body: details,
    async onResponse({ response }) {
        const data = response?._data as APIResponse
        if (data.statusCode === 200) {
            if (remember.value) setAuthCookie(data.body)
            useUser().value!.token = data.body
            if (redirect) {
                if (typeof redirect !== 'string') redirect = '/'
                await navigateTo(redirect)
            } else {
                await navigateTo('/')
            }
        } else {
            errors.value.add(data.body || 'An unknown error occurred')
        }
    },
    onResponseError(error) {
        console.error(error.response._data)
    }
})

async function submit() {
    if (loading.value) return
    loading.value = true
    await execute()
    loading.value = false
}

function clearErrors() {
    if (errors.value.size === 0) return
    errors.value = new Set()
}
</script>

<template>
    <Title>Login</Title>
    <section class="absolute w-full" style="margin-top: 100px">
        <div class="container mx-auto px-4 h-full">
            <div class="flex content-center items-center justify-center h-full">
                <div class="w-full lg:w-4/12 px-4">
                    <div
                        class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                        <div class="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                            <div class="text-gray-500 text-center mb-3 font-bold">
                                <small>Sign in with credentials</small>
                            </div>
                            <form>
                                <div class="text-red-500" v-if="errors.size > 0">
                                    <ul>
                                        <li v-for="error in errors" :key="error"><small>{{ error }}</small></li>
                                    </ul>
                                </div>
                                <div class="relative w-full mb-3">
                                    <label class="block uppercase text-gray-700 text-xs font-bold mb-2"
                                        for="grid-password">Email</label><input type="email"
                                        class="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                        placeholder="Email" v-model="details.email" v-on:focus="clearErrors"
                                        style="transition: all 0.15s ease 0s;" />
                                </div>
                                <div class="relative w-full mb-3">
                                    <label class="block uppercase text-gray-700 text-xs font-bold mb-2"
                                        for="grid-password">Password</label><input type="password"
                                        v-model="details.password"
                                        class="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                        placeholder="Password" v-on:focus="clearErrors"
                                        style="transition: all 0.15s ease 0s;" />
                                </div>
                                <div>
                                    <label class="inline-flex items-center cursor-pointer">
                                        <input id="customCheckLogin" type="checkbox" v-model="remember" checked
                                            class="form-checkbox border-0 rounded text-gray-800 ml-1 w-5 h-5"
                                            style="transition: all 0.15s ease 0s;" /><span
                                            class="ml-2 text-sm font-semibold text-gray-700">Remember me</span></label>
                                </div>
                                <div class="text-center mt-6">
                                    <button
                                        class="bg-gray-900 text-white active:bg-gray-700 text-sm font-bold uppercase px-6 py-3 rounded shadow hover:shadow-lg outline-none focus:outline-none mr-1 mb-1 w-full"
                                        type="button" @click="submit" style="transition: all 0.15s ease 0s;">
                                        <span v-if="!loading">Sign In</span>
                                        <span :class="{ 'loading': loading }" class="w-full grid place-items-center" v-else>
                                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                                                class="w-5 h-5">
                                                <path
                                                    d="M18.364 5.63604L16.9497 7.05025C15.683 5.7835 13.933 5 12 5C8.13401 5 5 8.13401 5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12H21C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C14.4853 3 16.7353 4.00736 18.364 5.63604Z">
                                                </path>
                                            </svg>
                                        </span>
                                    </button>
                                </div>
                            </form>
                        </div>
                    </div>
                    <div class="flex flex-wrap mt-6">
                        <div class="w-1/2">
                            <a class="text-slate-900"><small>Forgot password?</small></a>
                        </div>
                        <div class="w-1/2 text-right">
                            <NuxtLink class="text-slate-900" to="/signup"><small>Create new account</small></NuxtLink>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>

<style scoped>
.loading {
    @apply animate-spin;
}
</style>