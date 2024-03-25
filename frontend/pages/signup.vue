<script setup lang="ts">
import type { APIResponse } from '~/typings';

const url = useRoute()
const loading = ref(false)
let redirect = url.query?.redirect

const details = reactive({
    email: '',
    phone: '',
    password1: '',
    password2: ''
})

const body = computed(() => {
    return {
        email: details.email,
        phone: details.phone,
        password: details.password1
    }
})

const errors = ref(new Set())

const { execute } = await DeFetch(route('/api/auth/signup'), {
    method: 'POST',
    body: body,
    async onResponse({ response }) {
        const data = response._data as APIResponse
        if (data.statusCode === 201) {
            setAuthCookie(data.body)
            useUser().value!.token = data.body
            if (redirect) {
                if (typeof redirect !== 'string') redirect = '/'
                await navigateTo(redirect)
            } else {
                await navigateTo('/')
            }
        }
    },
    onResponseError(error){
        console.error(error.response._data)
        errors.value.add(JSON.stringify(error.response._data))
    }
})

async function submit() {
    if (errors.value.size > 0) return alert('Please fix the errors')
    loading.value = true
    await execute();
    loading.value = false
}


watch(details, () => {
    if (details.password2 !== '' && details.password1 !== details.password2) {
        errors.value.add('Passwords do not match')
    } else {
        errors.value.delete('Passwords do not match')
    }

    if (details.password1.length < 8) {
        errors.value.add('Password must be at least 8 characters')
    } else {
        errors.value.delete('Password must be at least 8 characters')
    }

    if ((details.email === '' && details.password1 !== '') || !details.email.includes('@')) {
        errors.value.add('Valid email is required')
    } else {
        errors.value.delete('Valid email is required')
    }
})
</script>

<template>
    <Title>Sign Up</Title>
    <section class="relative w-full" style="margin-top: 100px">
        <div class="container mx-auto px-4 h-full">
            <div class="flex content-center items-center justify-center h-full">
                <div class="w-full lg:w-4/12 px-4">
                    <div
                        class="relative flex flex-col min-w-0 break-words w-full mb-6 shadow-lg rounded-lg bg-gray-300 border-0">
                        <div class="flex-auto px-4 lg:px-10 py-10 pt-0 mt-6">
                            <div class="text-gray-500 text-center mb-3 font-bold">
                                <small>Sign up with credentials</small>
                            </div>
                            <form @submit.prevent="submit">
                                <div class="relative w-full mb-3">
                                    <label class="block uppercase text-gray-700 text-xs font-bold mb-2"
                                        for="grid-password">Email</label><input type="email" v-model="details.email"
                                        autocomplete="email"
                                        class="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                        placeholder="Email" style="transition: all 0.15s ease 0s;" />
                                </div>
                                <div class="relative w-full mb-3">
                                    <label class="block uppercase text-gray-700 text-xs font-bold mb-2"
                                        for="grid-password">Phone</label><input type="email" v-model="details.phone"
                                        autocomplete="tel"
                                        class="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                        placeholder="Phone" style="transition: all 0.15s ease 0s;" />
                                </div>
                                <div class="relative w-full mb-3">
                                    <label class="block uppercase text-gray-700 text-xs font-bold mb-2"
                                        for="grid-password">Password</label><input type="password"
                                        v-model="details.password1" autocomplete="new-password"
                                        class="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                        placeholder="Password" style="transition: all 0.15s ease 0s;" />
                                </div>
                                <div class="relative w-full mb-3">
                                    <label class="block uppercase text-gray-700 text-xs font-bold mb-2"
                                        for="grid-password">Password Again</label><input type="password"
                                        autocomplete="new-password" v-model="details.password2"
                                        class="border-0 px-3 py-3 placeholder-gray-400 text-gray-700 bg-white rounded text-sm shadow focus:outline-none focus:ring w-full"
                                        placeholder="Password" style="transition: all 0.15s ease 0s;" />
                                </div>
                                <div class="text-red-500" v-if="errors.size > 0">
                                    <ul>
                                        <li v-for="(error, index) in errors" :key="index"><small>{{ error }}</small></li>
                                    </ul>
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
                        <div class="w-full text-right">
                            <NuxtLink class="text-slate-900" to="/login"><small>Already Have an Account?</small></NuxtLink>
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
</style>DeezFetch