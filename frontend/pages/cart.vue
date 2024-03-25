<template>
    <Title>Cart</Title>
    <div class="container flex flex-col mx-auto p-4">
        <div class="flex mb-4">
            <button class="px-4 py-2 bg-amber-500 text-white rounded hover:bg-red-600 ml-5" @click="clearCart">
                Clear Cart
            </button>
            <button @click="checkout"
                class="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 flex items-center ml-auto">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor"
                    class="w-5 h-5 inline-block mr-2">
                    <path
                        d="M3.00488 3.00275H21.0049C21.5572 3.00275 22.0049 3.45046 22.0049 4.00275V20.0027C22.0049 20.555 21.5572 21.0027 21.0049 21.0027H3.00488C2.4526 21.0027 2.00488 20.555 2.00488 20.0027V4.00275C2.00488 3.45046 2.4526 3.00275 3.00488 3.00275ZM4.00488 5.00275V19.0027H20.0049V5.00275H4.00488ZM8.50488 14.0027H14.0049C14.281 14.0027 14.5049 13.7789 14.5049 13.5027C14.5049 13.2266 14.281 13.0027 14.0049 13.0027H10.0049C8.62417 13.0027 7.50488 11.8835 7.50488 10.5027C7.50488 9.12203 8.62417 8.00275 10.0049 8.00275H11.0049V6.00275H13.0049V8.00275H15.5049V10.0027H10.0049C9.72874 10.0027 9.50488 10.2266 9.50488 10.5027C9.50488 10.7789 9.72874 11.0027 10.0049 11.0027H14.0049C15.3856 11.0027 16.5049 12.122 16.5049 13.5027C16.5049 14.8835 15.3856 16.0027 14.0049 16.0027H13.0049V18.0027H11.0049V16.0027H8.50488V14.0027Z">
                    </path>
                </svg>
                Checkout
            </button>
        </div>
        <hr class="mb-4">
        <div class="flex flex-wrap gap-4">
            <ClientOnly>
                <div v-for="item in items" :key="item.id" class="bg-white p-4 rounded-lg border border-gray-200 w-[350px] px-4"
                    style="max-width: 330px;">
                    <img :src="route(item.image)" alt="" class="w-full h-40 object-cover rounded-lg">
                    <div class="mt-4">
                        <h3 class="text-lg font-semibold" style="text-transform: capitalize;">{{ item.name }}</h3>
                        <p class="text-sm text-gray-500">{{ item.description }}</p>
                        <div class="flex justify-between items-center mt-4">
                            <p class="text-lg font-bold">{{ item.price }}</p>
                            <p class="text-amber-500">{{ item.stock }} in Stock</p>
                            <button class="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
                                @click="removeFromCart(item.id)">Remove</button>
                        </div>
                    </div>
                </div>
            </ClientOnly>
        </div>
    </div>
</template>
<script setup lang="ts">
import type { APIResponse } from '~/typings';

definePageMeta({
    layout: 'dash'
})

const items = reactive(process.client ? JSON.parse(localStorage.getItem('cart') || '[]') : [])

function clearCart() {
    if (!process.client) return
    localStorage.removeItem('cart')
    items.splice(0, items.length)
}

function removeFromCart(id: number) {
    if (!process.client) return
    const index = items.findIndex((item: any) => item.id === id)
    items.splice(index, 1)
    localStorage.setItem('cart', JSON.stringify(items))
}

const { execute, data } = await DeFetch(route('/api/orders'), {
    method: 'POST',
    body: items,
    onResponseError(error) {
        console.error(error.response._data)
        alert('An error occurred while processing your order')
    }
})

async function checkout() {
    assertAuth('cart')
    if (items.length === 0) return
    await execute()

    const res = data.value as APIResponse

    if (res.statusCode === 200 || res.statusCode === 201) {
        localStorage.removeItem('cart')
        items.splice(0, items.length)
        alert('An SMS with your order details has been sent to your phone number')
        navigateTo('/orders')
    }
}
</script>