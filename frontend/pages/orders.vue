<template>
    <Title>Orders</Title>
    <div class="container flex flex-col mx-auto p-4">
        <div class="flex flex-wrap gap-4">
            <div v-for="item in items" :key="item.id" class="bg-white p-4 rounded-lg border border-gray-200 w-[350px] px-4"
                style="max-width: 330px;">
                <img :src="item.product.image" alt=""
                    class="w-full h-40 object-cover rounded-lg">
                <div class="mt-4">
                    <h3 class="text-lg font-semibold" style="text-transform: capitalize;">{{ item.product.name }}</h3>
                    <p class="text-sm text-gray-500">{{ new Date(item.time).toDateString() }}</p>
                    <div class="flex justify-between items-center mt-4">
                        <p class="text-lg font-bold">{{ item.price }}</p>
                        <p class="text-amber-500">{{ item.status }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup lang="ts">
import type { APIResponse } from '~/typings';

definePageMeta({
    layout: 'dash'
})

await assertAuth('orders')

const { data } = await useFetch<APIResponse>('/api/orders', {
    method: 'GET',
    headers: {
        'Authorization': 'Bearer ' + getAuthToken() || ''
    },
    onRequestError({ error }) {
        console.error(error)
    }
})
const items = data.value?.body
</script>